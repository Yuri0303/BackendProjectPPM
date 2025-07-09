from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}