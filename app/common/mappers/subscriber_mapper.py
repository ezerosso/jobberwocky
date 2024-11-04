from app.common.dtos.job_dto import SubscriberDTO
from app.domains.subsriber_domain import SubscriberDomain
from app.models.subscriber import Subscriber


class SubscriberMapper:    
    @staticmethod
    def from_sub_to_sub_domain(sub: Subscriber) -> SubscriberDomain:
        return SubscriberDomain(
            email=sub.email,
            search_pattern=sub.search_pattern,
        )
        
    @staticmethod
    def from_sub_domain_to_sub(sub: SubscriberDomain) -> Subscriber:
        return Subscriber(
            email=sub.email,
            search_pattern=sub.search_pattern,
        )
        
    @staticmethod
    def from_Subscriber_dto_to_subscriber_domain(subscriberDTO: SubscriberDTO) -> SubscriberDomain:
        return SubscriberDomain(email=subscriberDTO['email'], search_pattern=subscriberDTO['pattern'])