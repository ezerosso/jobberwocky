class BaseException(Exception):
    def __init__(self, message: str, code: str = None, error_code: str = None):
        self.message = message
        self.code = code
        self.error_code = error_code or "INTERNAL_ERROR"
        super().__init__(self.message)
        
class InvalidDataException(BaseException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code=400,
            error_code="INVALID_JOB_DATA"
        )