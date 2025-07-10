from flask_sqlalchemy import SQLAlchemy
from datetime import date, time

db = SQLAlchemy()

def to_dict(obj):
    result = {}
    for column in obj.__table__.columns:
        value = getattr(obj, column.name)
        if isinstance(value, (date, time)):
            value = value.isoformat()  # converte in stringa 'YYYY-MM-DD' o 'HH:MM:SS'
        result[column.name] = value
    return result