from src.domain.services import TeamGeneratorService
from src.domain.entities import Player, Team, Position
from src.domain.services import TeamConfiguration, InvalidTeamConfigurationError
import pytest
from src.infrastructure.repositories.in_memory import InMemoryPlayerRepository
from src.infrastructure.repositories.in_memory import InMemoryUniverseRepository
import re

@pytest.fixture
def player_repository(num_players: int = 5):
    repo = InMemoryPlayerRepository(universe_repository=InMemoryUniverseRepository())
    test_players = [
        Player(name="Player 1", height=180.0, weight=80.0, universe_id="test_universe"),
        Player(name="Player 2", height=185.0, weight=85.0, universe_id="test_universe"),
        Player(name="Player 3", height=170.0, weight=75.0, universe_id="test_universe"),
        Player(name="Player 4", height=175.0, weight=82.0, universe_id="test_universe"),
        Player(name="Player 5", height=182.0, weight=88.0, universe_id="test_universe")
    ]
    for player in test_players:
        repo.add(player)
    return repo


def test_generate_team(player_repository):
    service = TeamGeneratorService()
    team = service.generate_team("test_universe", TeamConfiguration(defenders=2, attackers=2, total_players=5), player_repository.get_all_by_universe("test_universe"))
    assert len(team.players) == 5
    assert team.goalie is not None
    assert len(team.defenders) == 2
    assert len(team.attackers) == 2

def test_generate_team_raises_when_not_enough_players(player_repository):
    service = TeamGeneratorService()
    
    error_message = "Team must have exactly 4 field players (defenders + attackers)"
    with pytest.raises(InvalidTeamConfigurationError, match=re.escape(error_message)):
        service.generate_team("test_universe", TeamConfiguration(defenders=1, attackers=1, total_players=3), player_repository.get_all_by_universe("test_universe")[:2])

def test_generate_team_raises_when_too_many_players(player_repository):
    service = TeamGeneratorService()
    error_message = "Team must have exactly 4 field players (defenders + attackers)"
    with pytest.raises(InvalidTeamConfigurationError, match=re.escape(error_message)):
        service.generate_team("test_universe", TeamConfiguration(defenders=3, attackers=3, total_players=5), player_repository.get_all_by_universe("test_universe"))

def test_goalie_is_the_tallest_player(player_repository):
    service = TeamGeneratorService()
    team = service.generate_team("test_universe", TeamConfiguration(defenders=2, attackers=2, total_players=5), player_repository.get_all_by_universe("test_universe"))
    assert team.goalie.height == max(player.height for player in team.players)

def test_defenders_are_the_heaviest_players(player_repository):
    service = TeamGeneratorService()
    team = service.generate_team("test_universe", TeamConfiguration(defenders=2, attackers=2, total_players=5), player_repository.get_all_by_universe("test_universe"))
    assert max([player.weight for player in team.defenders]) > max([player.weight for player in team.attackers])

def test_offensive_team_has_more_attackers_than_defenders(player_repository):
    service = TeamGeneratorService()
    team = service.generate_team("test_universe", TeamConfiguration(defenders=1, attackers=3, total_players=5), player_repository.get_all_by_universe("test_universe"))
    assert len(team.attackers) > len(team.defenders)
