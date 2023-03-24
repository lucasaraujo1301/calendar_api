import psycopg2.errors
from flask import Blueprint, jsonify, g, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from psycopg2 import errorcodes

from calendar_api.data_classes.user import UserLoginRequest, CreateUserRequest
from calendar_api.decorators.validate_request import validate_json

app = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/login', methods=['POST'])
@validate_json(UserLoginRequest)
def login(user_request: UserLoginRequest):
    try:
        user_uuid = g.core.auth_use_case().login(user_request)
        access_token = create_access_token(identity=user_uuid)
        return jsonify(access_token=access_token), 200
    except Exception:
        abort(401)


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


@app.route('/protect')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
