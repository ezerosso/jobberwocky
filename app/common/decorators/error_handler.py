from flask import Blueprint
from app.common.exceptions.base_exception import BaseException
from app.common.response.api_response import ApiResponse
import traceback
from app.common.logger import logger

error_handlers = Blueprint('error_handlers', __name__)

@error_handlers.app_errorhandler(BaseException)
def handle_base_exception(error):
    return ApiResponse.error(
        message=error.message,
        code=error.code,
        error_code=error.error_code
    )

@error_handlers.app_errorhandler(Exception)
def handle_generic_error(error):
    logger.error(f"Unexpected error: {str(error)}\n{traceback.format_exc()}")
    return ApiResponse.error(
        message="An unexpected error occurred",
        code=500,
        error_code="INTERNAL_SERVER_ERROR"
    )