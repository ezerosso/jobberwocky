from app.common.logger import logger
from app.common.dtos.job_dto import SubscriberDTO
from app.common.exceptions.base_exception import InvalidDataException
from app.common.mappers.subscriber_mapper import SubscriberMapper
from app.interfaces.subscriber_repository_interface import SubscriberRepositoryInterface
from app.common.decorators.transaction import transactional
from app.common.exceptions.subscriber_exception import DuplicateSubscriberException

class SubscriberService:
    def __init__(self, subscriber_repository: SubscriberRepositoryInterface):
        self.subscriber_repository = subscriber_repository

    @transactional
    def subscribe(self, subscriber_dto: SubscriberDTO) -> None:
        
        subscriber = SubscriberMapper.from_Subscriber_dto_to_subscriber_domain(subscriber_dto)
        
        if self.subscriber_repository.exists_subscriber(subscriber):
            raise DuplicateSubscriberException("subscriber already exist")
        
        try:
            self.subscriber_repository.create(subscriber)
        except Exception as e:
            logger.error(f"Error in create subscribers: {str(e)}")
            raise InvalidDataException(f"Failed to create subscriber")
        