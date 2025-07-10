from flask.views import MethodView
from flask import request, jsonify, Blueprint, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models.user import User
from models.forecast import Forecast
from models.location import Location
from models.query_log import QueryLog
from models.daily_ip_request import DailyIpRequest
from datetime import date, datetime
from db import db, to_dict

bp = Blueprint('forecast', __name__, url_prefix='/api')

class ForecastView(MethodView):
    def get(self):
        resp = make_response({"user": "demo"})
        resp.headers['Access-Control-Allow-Origin'] = 'https://yuri0303.github.io'
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        return resp

        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except Exception:
            user_id = None #Public user

        data = request.args
        location_name = data.get('location')
        date_str = data.get('date')
        time_str = data.get('time')

        forecast_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        forecast_time = datetime.strptime(time_str, '%H:%M').time()

        location: Location = Location.query.filter_by(name=location_name).first()
        if location is None:
            return jsonify({'msg': f'Location: {location_name} not found'}), 404

        if not all([forecast_date, forecast_time]):
            return jsonify({'msg': 'Missing parameters'}), 400

        forecast: Forecast = Forecast.query.filter_by(location_id=location.id, date=forecast_date, time=forecast_time).first()
        if forecast is None:
            return jsonify({'msg': 'No forecast found'}), 404

        if user_id:
            if User.query.filter_by(id=user_id).first().is_admin:
                return jsonify({'msg': 'Admin can\'t save queries. Please log in with a Premium user account'}), 403
            if QueryLog.query.filter_by(user_id=user_id, forecast_id=forecast.id).first() is None:
                query = QueryLog(user_id=user_id, forecast_id = forecast.id)
                db.session.add(query)
                db.session.commit()
        else:
            ip = request.remote_addr
            today = date.today()
            record: DailyIpRequest = DailyIpRequest.query.filter_by(ip=ip, date=today).first()
            if record:
                if record.count >= 10:
                    return jsonify({'msg': 'Daily request limit reached (10)'}), 429
                else:
                    record.count += 1
            else:
                record = DailyIpRequest(ip=ip, date=today, count=1)
                db.session.add(record)

            db.session.commit()

        return jsonify(to_dict(forecast))

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user: User = User.query.filter_by(id=user_id).first()

        if not user.is_admin:
            return jsonify({'msg': 'Only Admin can add forecasts'}), 403

        data = request.get_json()

        location_name = data.get('location')
        temperature = data.get('temperature')
        condition = data.get('condition')
        rain = data.get('rain')

        date_str = data.get('date')
        time_str = data.get('time')

        forecast_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        forecast_time = datetime.strptime(time_str, '%H:%M').time()

        location: Location = Location.query.filter_by(name=location_name).first()
        if not location:
            return jsonify({'msg': f'Location:{location_name} not found'}), 404

        if not all([forecast_date, forecast_time, temperature, condition, rain]):
            return jsonify({'msg': 'Missing parameters'}), 400

        forecast = Forecast(location_id=location.id,
                            date=forecast_date,
                            time=forecast_time,
                            temperature=temperature,
                            condition=condition,
                            rain=rain)
        db.session.add(forecast)
        db.session.commit()

        return jsonify({'msg': 'Forecast added successfully'}), 201

bp.add_url_rule('/forecast', view_func=ForecastView.as_view('forecast'))


@bp.route('/savedQueries', methods=['GET'])
@jwt_required()
def saved_queries():
    user_id = get_jwt_identity()

    if User.query.filter_by(id=user_id).first().is_admin:
        return jsonify({'msg': 'Admin don\'t have saved queries. Please log in with a Premium User account'}), 403

    logs = QueryLog.query.filter_by(user_id=user_id).all()

    if not logs:
        return jsonify({'msg': 'No saved queries'}), 404

    result = []
    for query in logs:
        forecast = Forecast.query.filter_by(id=query.forecast_id).first()
        result.append(to_dict(forecast))

    return jsonify(result)

@bp.route('/location', methods=['POST'])
@jwt_required()
def add_location():
    user_id = get_jwt_identity()
    user: User = User.query.filter_by(id=user_id).first()

    if not user.is_admin:
        return jsonify({'msg': 'Only admin can add locations'}), 403

    data = request.get_json()

    location_name = data.get('name')
    location_lat = data.get('lat')
    location_lon = data.get('lon')

    if not all([location_name, location_lat, location_lon]):
        return jsonify({'msg': 'Missing parameters'}), 400

    location = Location(name=location_name, lat=location_lat, lon=location_lon)
    db.session.add(location)
    db.session.commit()

    return jsonify({'msg': 'Location added successfully'}), 201

@bp.route('/userinfo')
@jwt_required()
def user_info():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    return jsonify(to_dict(user)), 200