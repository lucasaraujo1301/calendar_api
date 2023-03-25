from flask import request, jsonify, abort
from functools import wraps

from flask_jwt_extended import get_jwt

from calendar_lib.data_classes.user import GroupEnum


def validate_json(cls):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json_data = request.get_json()
            try:
                obj = cls(**json_data)
            except TypeError as e:
                return jsonify({'error': str(e)}), 422
            return f(obj, *args, **kwargs)

        return wrapper

    return decorator


def group_required(group_name):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            # # Verify that a valid JWT is present in the request
            # verify_jwt_in_request()

            # Get the user's claims from the JWT
            claims = get_jwt()

            # Check if the user has the required group
            if GroupEnum(group_name) not in GroupEnum.__members__.values():
                abort(500, description=f'Invalid group name: {group_name}')
            if claims['group'] != group_name:
                abort(403,
                      description=f'You do not have permission to perform this action. Required group: {group_name}')

            return fn(*args, **kwargs)
        return wrapper
    return decorator
