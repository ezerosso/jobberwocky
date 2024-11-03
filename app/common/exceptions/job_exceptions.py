from app.common.exceptions.base_exception import BaseException

class JobNotFoundException(BaseException):
    def __init__(self, job_id: int):
        super().__init__(f"Job with id {job_id} not found", "JOB_NOT_FOUND")
        
class DuplicateJobException(BaseException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code=400,
            error_code="INVALID_JOB"
        )
        
class InvalidSearchException(BaseException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code=400,
            error_code="INVALID_JOB_DATA"
        )