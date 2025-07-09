from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import db

class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)
    lat: Mapped[float] = mapped_column(nullable=False)
    lon: Mapped[float] = mapped_column(nullable=False)

    forecasts = relationship('Forecast', backref='location')