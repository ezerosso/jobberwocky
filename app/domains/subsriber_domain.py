
from typing import Optional


class SubscriberDomain:
    def __init__(self, 
                 email: str, 
                 search_pattern: str, 
                 id: Optional[int] = None) : 
        self.id = id
        self.email = email
        self.search_pattern = search_pattern