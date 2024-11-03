from typing import Any, Optional
from flask import jsonify

class ApiResponse:
    @staticmethod
    def success(data: Any = None, status_code: int = 200):
        response = {
            "success": True,
            "data": data
        }
        return jsonify(response), status_code

    @staticmethod
    def error(message: str, code: int = 400, error_code: str = "INTERNAL_ERROR"):
        response = {
            "success": False,
            "error": {
                "message": message,
                "code": error_code
            }
        }
        return jsonify(response), code