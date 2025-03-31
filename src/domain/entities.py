from src.domain.base import BaseEntity
from uuid import UUID

class Universe(BaseEntity):
    name: str
    description: str


class Team(BaseEntity):
    name: str
    description: str
    universe_id: UUID
    universe: Universe
    
    
class Player(BaseEntity):
    name: str
    description: str
    universe_id: UUID
    universe: Universe