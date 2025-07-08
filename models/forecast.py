from sqlalchemy import Date, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import time
from db import db

class Forecast(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(ForeignKey('location.id'), nullable=False)

    date: Mapped[Date] = mapped_column(nullable=False)
    time: Mapped[Time] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    condition: Mapped[str] = mapped_column(nullable=False)
    rain: Mapped[float] = mapped_column(nullable=False)
