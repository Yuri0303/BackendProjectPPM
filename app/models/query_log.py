from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from db import db

class QueryLog(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    forecast_id: Mapped[int] = mapped_column(ForeignKey('forecast.id'), nullable=False)

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)