from flask_sqlalchemy import SQLAlchemy
from app.user.dao import UserDAO
from app.user.model import User
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:
    def __init__(self, db: SQLAlchemy):
        self.dao = UserDAO(db)

    def register(self, new_user) -> tuple[None, str, int] | tuple[User, str, int]:
        user = self.dao.get_by_username(new_user.username)
        if user:
            return None, "Username already exists", 400

        user_to_create = User(username=new_user.username)
        user_to_create.set_password(new_user.password)

        user = self.dao.register(user_to_create)

        return user.to_dict(), "User register successfully", 201

    def login(self, user_dto) -> tuple[None, str, int] | tuple[User, str, int]:
        user = self.dao.get_by_username(user_dto.username)

        if not user:
            return None, "Username not found", 404

        if check_password_hash(user.password_hash, user_dto.password):
            return user.to_dict(), "User login successfully", 200
        else:
            return None, "Wrong password", 403

    def get_all(self):
        users = self.dao.get_all()

        return [user.to_dict() for user in users]