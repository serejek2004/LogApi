from app import app, db
from flask import request, jsonify
from app.user.dto import UserDTO
from app.user.service import UserService

UserService = UserService(db)


@app.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    user_dto = UserDTO.from_request(data)
    user, status_code = UserService.register(user_dto)

    return jsonify(user.to_dict()), status_code


@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    user_dto = UserDTO.from_request(data)
    access_token, status_code = UserService.login(user_dto)

    return jsonify({"access_token": access_token}), status_code


@app.route('/user', methods=['GET'])
def get_all():
    users = UserService.get_all()

    return jsonify(users), 200
