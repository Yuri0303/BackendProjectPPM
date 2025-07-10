from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from db import db
from models.user import create_admin
from auth.routes import bp as auth_bp
from forecast_api.routes import bp as forecast_bp
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')

jwt = JWTManager(app)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(forecast_bp)

CORS(app, supports_credentials=True)

with app.app_context():
    db.create_all()
    create_admin()


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405

@app.route('/')
def hello_world():
    return jsonify({"msg": "Check documentation to start using Weather API"})


if __name__ == '__main__':
    app.run()
