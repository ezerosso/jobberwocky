from app.common.exceptions.base_exception import BaseException


class ExternalServiceException(BaseException):
    def __init__(self, service_name: str, message: str):
        super().__init__(f"Error in external service {service_name}: {message}", "EXTERNAL_SERVICE_ERROR")
