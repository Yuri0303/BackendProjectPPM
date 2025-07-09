from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from db import db

class DailyIpRequest(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(nullable=False)

    date: Mapped[date] = mapped_column(Date, nullable=False)
    count: Mapped[int] = mapped_column(default=1)