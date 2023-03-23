from flask import request, jsonify
from functools import wraps


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
