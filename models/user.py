from db import db
from sqlalchemy.orm import mapped_column, Mapped, relationship
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    query_logs = relationship('QueryLog', backref='user')
    daily_user_request = relationship('DailyUserRequest', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)