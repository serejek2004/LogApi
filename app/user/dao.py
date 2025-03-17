from flask_sqlalchemy import SQLAlchemy
from app.user.model import User


class UserDAO:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all(self):
        return self.db.session.query(User).all()

    def get_by_username(self, username: str) -> User | None:
        return self.db.session.query(User).filter_by(username=username).first()

    def register(self, user: User) -> User:
        self.db.session.add(user)
        self.db.session.commit()
        return user

