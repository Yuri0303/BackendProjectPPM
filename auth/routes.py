from flask import Blueprint, request, jsonify
from db import db
from models.user import User
from flask_jwt_extended import create_access_token

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exist'}), 409

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user: User = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Wrong username or password'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access token': access_token, 'type': user.type}), 200
