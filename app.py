from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from db import db
from auth.routes import bp as auth_bp
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

jwt = JWTManager(app)

db.init_app(app)

app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
