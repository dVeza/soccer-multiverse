from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.infrastructure.db.database import get_db
from src.api.schemas import TeamResponse, UniverseResponse, TeamConfigurationRequest
from src.domain.services import TeamGeneratorService, TeamConfiguration, InvalidTeamConfigurationError
from src.infrastructure.repositories.orm import SQLAlchemyUniverseRepository, SQLAlchemyPlayerRepository
from pydantic import ValidationError
from typing import Optional

router = APIRouter()

# Create repository factory functions
def get_universe_repository(db: Session = Depends(get_db)):
    return SQLAlchemyUniverseRepository(db)

def get_player_repository(db: Session = Depends(get_db)):
    return SQLAlchemyPlayerRepository(db)

# First, create a dependency function that handles the raw query params
async def get_team_config(
    defenders: Optional[int] = Query(default=2),
    attackers: Optional[int] = Query(default=2)
) -> TeamConfigurationRequest:
    try:
        return TeamConfigurationRequest(defenders=defenders, attackers=attackers)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e.errors()))

@router.get("/teams/generate/{universe_name}")
def generate_team(
    universe_name: str,
    config: TeamConfigurationRequest = Depends(get_team_config),
    universe_repo = Depends(get_universe_repository),
    player_repo = Depends(get_player_repository)
) -> TeamResponse:
    """Generate a random team for specified universe"""
    try:
        team_service = TeamGeneratorService()
        universe = universe_repo.get_by_name(universe_name)
        if not universe:
            raise HTTPException(status_code=404, detail="Universe not found")
        
        players = player_repo.get_random_by_universe(universe.id, 5)
        team_config = TeamConfiguration(
            defenders=config.defenders,
            attackers=config.attackers,
            total_players=5
        )
        
        team = team_service.generate_team(universe.id, team_config, players)
        return TeamResponse.from_domain(team)
    
    except InvalidTeamConfigurationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/universes")
def list_universes(
    universe_repo = Depends(get_universe_repository)
) -> list[UniverseResponse]:
    """List all available universes"""
    return universe_repo.list() 