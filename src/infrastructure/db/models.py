from uuid import uuid4
from sqlalchemy import Column, String, Float, ForeignKey, Table, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.infrastructure.db.database import Base
from src.domain.entities import Position

# First, create the enum type
position_enum = Enum(
    Position,
    name='position_type',  # This is the name of the enum type in the database
    create_type=True,      # This tells SQLAlchemy to create the type in the database
    native_enum=True       # Use PostgreSQL's native enum type
)

# Then use it in your table
team_players = Table(
    'team_players',
    Base.metadata,
    Column('team_id', UUID, ForeignKey('teams.id')),
    Column('player_id', UUID, ForeignKey('players.id')),
    Column('position', position_enum, nullable=False)  # Use the enum we created
)


class UniverseModel(Base):
    __tablename__ = "universes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

class PlayerModel(Base):
    __tablename__ = "players"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    universe_id = Column(UUID(as_uuid=True), ForeignKey("universes.id"), nullable=False)

class TeamModel(Base):
    __tablename__ = 'teams'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String)
    universe_id = Column(UUID(as_uuid=True), ForeignKey("universes.id"))
    players = relationship(
        'PlayerModel',
        secondary=team_players,
        backref='teams'
    ) 