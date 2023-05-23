import datetime

import psycopg2.errors
from flask import Blueprint, jsonify, g
from flask_jwt_extended import create_access_token

from calendar_lib.data_classes.user import UserLoginRequest, CreateUserRequest
from calendar_api.decorators.validate_request import validate_json

app = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/login', methods=['POST'])
@validate_json(UserLoginRequest)
def login(user_request: UserLoginRequest):
    try:
        user = g.core.auth_use_case().login(user_request)
        access_token = create_access_token(
            identity=user.uuid,
            additional_claims={
                'group': user.group_name,
                'created_at': datetime.datetime.now()
            }
        )
        return jsonify(access_token=access_token), 200
    except Exception as e:
        return jsonify(message=str(e)), 401


@app.route('/register', methods=['POST'])
@validate_json(CreateUserRequest)
def register(user_request: CreateUserRequest):
    try:
        result, error = g.core.auth_use_case().register(user_request)
        if error:
            return jsonify({'errors': error}), 409
        return jsonify({'message': 'success'}), 200
    except psycopg2.Error as e:
        return jsonify(message=e.pgerror), 400
