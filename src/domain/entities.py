from uuid import UUID
from datetime import datetime
import uuid
from typing import List, Optional
from enum import Enum

class BaseEntity:
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    def __init__(self, id: UUID = None):
        self.id = id if id else uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

class Universe(BaseEntity):
    name: str
    description: str

    def __init__(self, name: str, description: str, id: UUID = None):
        super().__init__(id)
        self.name = name
        self.description = description

class Position(Enum):
    GOALIE = "GOALIE"
    DEFENCE = "DEFENCE"
    OFFENCE = "OFFENCE"


class Player(BaseEntity):
    name: str
    height: float
    weight: float
    universe_id: UUID
    position: Position | None = None
    
    def __init__(self, name: str, height: float, weight: float, universe_id: UUID, id: UUID = None):
        super().__init__(id)
        self.name = name
        self.height = height
        self.weight = weight
        self.universe_id = universe_id


class Team(BaseEntity):
    name: str
    universe_id: UUID
    players: List[Player]
    
    def __init__(self, name: str, universe_id: UUID, id: UUID = None):
        super().__init__(id)
        self.name = name
        self.universe_id = universe_id
        self.players = []
        self._goalie: Optional[Player] = None
        self._defenders: List[Player] = []
        self._attackers: List[Player] = []

    def add_player(self, player: Player, position: Position) -> None:
        if player.universe_id != self.universe_id:
            raise ValueError("Player must be from the same universe")
            
        player.position = position
            
        if position == Position.GOALIE:
            if self._goalie is not None:
                raise ValueError("Team already has a goalie")
            self._goalie = player
        elif position == Position.DEFENCE:
            self._defenders.append(player)
        elif position == Position.OFFENCE:
            self._attackers.append(player)
            
        self.players.append(player)

    @property
    def goalie(self) -> Optional[Player]:
        return self._goalie

    @property
    def defenders(self) -> List[Player]:
        return self._defenders.copy()

    @property
    def attackers(self) -> List[Player]:
        return self._attackers.copy()

