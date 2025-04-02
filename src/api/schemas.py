from pydantic import BaseModel, field_validator
from src.domain.entities import Team, Universe, Player
from uuid import UUID
from typing import Optional

class PlayerBase(BaseModel):
    name: str
    height: float
    weight: float
    position: str

    class Config:
        from_attributes = True

class PlayerResponse(BaseModel):
    name: str
    weight: float
    height: float
    position: str

    @classmethod
    def from_domain(cls, player: Player):
        return cls(
            name=player.name,
            weight=player.weight,
            height=player.height,
            position=player.position
        )

class TeamResponse(BaseModel):
    players: list[PlayerResponse]

    @classmethod
    def from_domain(cls, team: Team):
        return cls(
            players=[PlayerResponse.from_domain(p) for p in team.players]
        )

class UniverseResponse(BaseModel):
    id: UUID
    name: str
    description: str | None

    @classmethod
    def from_domain(cls, universe: Universe):
        return cls(id=universe.id, name=universe.name, description=universe.description)

class TeamConfigurationRequest(BaseModel):
    defenders: Optional[int] = 2
    attackers: Optional[int] = 2
    
    @field_validator('defenders')
    def validate_defenders(cls, v):
        if v > 4:
            raise ValueError("Maximum 4 defenders allowed")
        if v < 0:
            raise ValueError("Number of defenders cannot be negative")
        return v
    
    @field_validator('attackers')
    def validate_attackers(cls, v, info):
        if v > 4:
            raise ValueError("Maximum 4 attackers allowed")
        if v < 0:
            raise ValueError("Number of attackers cannot be negative")
        
        # Get defenders value from info
        defenders = info.data.get('defenders', 2)  # Default to 2 if not set
        if defenders + v != 4:
            raise ValueError("Team must have exactly 4 field players (defenders + attackers)")
        return v 