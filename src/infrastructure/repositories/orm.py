from src.domain.repositories import AbstractRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from sqlalchemy import select
from src.domain.entities import BaseEntity
from typing import TypeVar
from uuid import UUID
from sqlalchemy.orm import Session
from src.domain.repositories import PlayerRepository, UniverseRepository
from src.domain.entities import Player, Universe
from src.infrastructure.db.models import PlayerModel, UniverseModel
import random


class SQLAlchemyUniverseRepository(UniverseRepository):
    def __init__(self, session: Session):
        self.model = UniverseModel
        self.session = session

    def add(self, universe: Universe) -> Universe:
        db_universe = UniverseModel(
            id=universe.id,
            name=universe.name,
            description=universe.description
        )
        self.session.add(db_universe)
        self.session.commit()
        return universe
    
    def list(self) -> List[Universe]:
        return [self._to_entity(u) for u in self.session.query(UniverseModel).all()]

    def get_by_id(self, id: UUID) -> Optional[Universe]:
        db_universe = self.session.query(UniverseModel).filter(UniverseModel.id == id).first()
        return Universe(db_universe.name, db_universe.description, db_universe.id) if db_universe else None

    def get_by_name(self, name: str) -> Optional[Universe]:
        db_universe = self.session.query(UniverseModel).filter(UniverseModel.name.ilike(name)).first()
        return Universe(
            name=db_universe.name,
            description=db_universe.description,
            id=db_universe.id
        ) if db_universe else None
    
    def _to_entity(self, model: UniverseModel) -> Universe:
        return Universe(
            name=model.name,
            description=model.description,
            id=model.id
        )


class SQLAlchemyPlayerRepository(PlayerRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, player: Player) -> Player:
        db_player = PlayerModel(
            id=player.id,
            name=player.name,
            height=player.height,
            weight=player.weight,
            universe_id=player.universe_id
        )
        self.session.add(db_player)
        self.session.commit()
        return player

    def get_by_id(self, id: str) -> Optional[Player]:
        db_player = self.session.query(PlayerModel).filter(PlayerModel.id == id).first()
        return self._to_entity(db_player) if db_player else None

    def list(self) -> List[Player]:
        return [self._to_entity(p) for p in self.session.query(PlayerModel).all()]

    def get_all_by_universe(self, universe_id: str) -> List[Player]:
        players = self.session.query(PlayerModel).filter(PlayerModel.universe_id == universe_id).all()
        return [self._to_entity(p) for p in players]

    def get_random_by_universe(self, universe_id: str, count: int) -> List[Player]:
        players = self.get_all_by_universe(universe_id)
        if len(players) < count:
            raise ValueError(f"Not enough players in universe {universe_id}")
        return random.sample(players, count)

    def _to_entity(self, model: PlayerModel) -> Player:
        return Player(
            name=model.name,
            height=model.height,
            weight=model.weight,
            universe_id=model.universe_id,
            id=model.id
        )

    def count_by_universe(self, universe_id: int) -> int:
        return self.session.query(PlayerModel).filter(PlayerModel.universe_id == universe_id).count()
