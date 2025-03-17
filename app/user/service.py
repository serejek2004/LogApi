from flask_sqlalchemy import SQLAlchemy
from app.user.dao import UserDAO
from app.user.model import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token


class UserService:
    def __init__(self, db: SQLAlchemy):
        self.dao = UserDAO(db)

    def register(self, new_user) -> tuple[None, int] | tuple[User, int]:
        user = self.dao.get_by_username(new_user.username)
        if user:
            return None, 400

        user_to_create = User(username=new_user.username)
        user_to_create.set_password(new_user.password)

        user = self.dao.register(user_to_create)

        return user, 201

    def login(self, user_dto) -> tuple[None, int] | tuple[str, int]:
        user = self.dao.get_by_username(user_dto.username)

        if not user:
            return None, 404

        if check_password_hash(user.password_hash, user_dto.password):
            access_token = create_access_token(identity=user.username)
            return access_token, 200
        else:
            return None, 403

    def get_all(self):
        users = self.dao.get_all()

        return [user.to_dict() for user in users]
