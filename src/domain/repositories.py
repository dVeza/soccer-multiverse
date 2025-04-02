from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from src.domain.entities import BaseEntity, Team, Universe, Player
from uuid import UUID

T = TypeVar('T', bound=BaseEntity)

class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]:
        pass
    
    @abstractmethod
    def list(self) -> List[T]:
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        pass



class TeamRepository(AbstractRepository[Team], ABC):
    @abstractmethod
    def get_by_universe(self, universe: str) -> List[Team]:
        pass


class UniverseRepository(AbstractRepository[Universe], ABC):
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Universe]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Universe]:
        pass

    @abstractmethod
    def list(self) -> List[Universe]:
        pass

    @abstractmethod
    def add(self, universe: Universe) -> Universe:
        pass


class PlayerRepository(AbstractRepository[Player], ABC):
    @abstractmethod
    def get_random_by_universe(self, universe: str, count: int) -> List[Player]:
        pass

    @abstractmethod
    def get_all_by_universe(self, universe: str) -> List[Player]:
        pass
