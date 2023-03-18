from flask import Blueprint, request, jsonify, g, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from calendar_api.data_classes.user import UserLoginRequest

app = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/login', methods=['POST'])
def register():
    user_request = request.get_json()
    try:
        user_request = UserLoginRequest(**user_request)
    except Exception:
        abort(400)

    try:
        user_uuid = g.core.auth_use_case().login(user_request)
        access_token = create_access_token(identity=user_uuid)
        return jsonify(access_token=access_token), 200
    except Exception:
        abort(404)


@app.route('/protect')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
