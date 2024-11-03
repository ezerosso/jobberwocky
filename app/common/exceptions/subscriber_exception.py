from app.common.exceptions.base_exception import BaseException

class DuplicateSubscriberException(BaseException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code=400,
            error_code="DUPLICATE_SUBSCRIBER"
        )