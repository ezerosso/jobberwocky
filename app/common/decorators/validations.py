from functools import wraps
from flask import request
from app.common.exceptions.base_exception import InvalidDataException

def validate_request(dto_class):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            dto = dto_class()
            errors = dto.validate(request.json)
            if errors:
                raise InvalidDataException(errors)
            validated_data = dto.load(request.json)
            return f(*args, validated_data, **kwargs)
        return decorated_function
    return decorator