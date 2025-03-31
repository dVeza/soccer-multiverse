from src.domain.entities import Universe, Player, Team
from uuid import UUID
from datetime import datetime


base_fields = ["id", "created_at", "updated_at"]


def test_universe_fields():
    universe = Universe(name="Marvel", description="A universe of superheroes")
    assert universe.name == "Marvel"
    assert universe.description == "A universe of superheroes"
    assert isinstance(universe.id, UUID)
    assert isinstance(universe.created_at, datetime)
    assert isinstance(universe.updated_at, datetime)


def test_team_fields():
    team = Team(name="Avengers", description="A team of superheroes", universe_id=UUID("123e4567-e89b-12d3-a456-426614174000"))
    assert team.name == "Avengers"
    assert team.description == "A team of superheroes"
    assert team.universe_id == UUID("123e4567-e89b-12d3-a456-426614174000")
    assert isinstance(team.id, UUID)
    assert isinstance(team.created_at, datetime)
    assert isinstance(team.updated_at, datetime)


def test_player_fields():
    player = Player(name="Iron Man", description="A superhero", universe_id=UUID("123e4567-e89b-12d3-a456-426614174000"))
    assert player.name == "Iron Man"