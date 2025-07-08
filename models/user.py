from db import db
from sqlalchemy.orm import mapped_column, Mapped
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False, default='anonymous')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)