from app.common.mappers.subscriber_mapper import SubscriberMapper
from app.domains.subsriber_domain import SubscriberDomain
from app.interfaces.subscriber_repository_interface import SubscriberRepositoryInterface
from app.models.subscriber import Subscriber
from app import db
from typing import List, Optional

class SQLiteSubscriberRepository(SubscriberRepositoryInterface):
    def create(self, subscriberDomain: SubscriberDomain) -> SubscriberDomain:
        subscriber = SubscriberMapper.from_sub_domain_to_sub(subscriberDomain)
        db.session.add(subscriber)
        db.session.commit()
        return

    def get_all(self) -> List[Subscriber]:
        return Subscriber.query.all()

    def find_by_id(self, subscriber_id: int) -> Optional[Subscriber]:
        return Subscriber.query.get(subscriber_id)

    def get_all_active_subscribers(self) -> List[Subscriber]:
        return db.session.query(Subscriber).all()

    def exists_subscriber(self, subscriberDomain: SubscriberDomain) -> bool:
        subscriber = SubscriberMapper.from_sub_domain_to_sub(subscriberDomain)
        existing_subscriber = db.session.query(Subscriber).filter_by(
            email=subscriber.email
        ).first()
        return existing_subscriber is not None