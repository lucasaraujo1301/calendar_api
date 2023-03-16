from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

app = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/login', methods=['POST'])
def register():
    username = request.json.get("username", None)

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route('/protect')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
