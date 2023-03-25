from uuid import UUID

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from calendar_api.decorators.validate_request import group_required

app = Blueprint('user', __name__, url_prefix='/user')


@app.route('/update/<uuid:user_uuid>', methods=['POST'])
@jwt_required()
@group_required('Admin')
def update_user(user_uuid: UUID):
    response = {'message': 'Ok', 'user_uuid': str(user_uuid)}
    return jsonify(response), 200
