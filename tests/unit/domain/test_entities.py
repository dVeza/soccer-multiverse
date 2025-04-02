from src.domain.entities import Universe, Player, Team
from uuid import UUID
from datetime import datetime


BASE_ENTITY_FIELDS = {
    "id": UUID,
    "created_at": datetime,
    "updated_at": datetime
}

UNIVERSE_FIELDS = {
    **BASE_ENTITY_FIELDS,
    "name": str,
    "description": str
}

TEAM_FIELDS = {
    **BASE_ENTITY_FIELDS,
    "name": str,
    "universe_id": UUID
}

PLAYER_FIELDS = {
    **BASE_ENTITY_FIELDS,
    "name": str,
    "universe_id": UUID,
    "height": float,
    "weight": float
}


def test_universe_fields():
    universe = Universe(name="Marvel", description="A universe of superheroes")
    assert universe.name == "Marvel"
    assert universe.description == "A universe of superheroes"
    assert isinstance(universe.id, UUID)
    assert isinstance(universe.created_at, datetime)
    assert isinstance(universe.updated_at, datetime)

    for field, field_type in UNIVERSE_FIELDS.items():
        assert isinstance(getattr(universe, field), field_type)


def test_team_fields():
    team = Team(name="Avengers", universe_id=Universe(name="Marvel", description="A universe of superheroes").id)
    assert team.name == "Avengers"
    assert isinstance(team.id, UUID)
    assert isinstance(team.created_at, datetime)
    assert isinstance(team.updated_at, datetime)
    assert isinstance(team.universe_id, UUID)

    for field, field_type in TEAM_FIELDS.items():
        assert isinstance(getattr(team, field), field_type)

def test_player_fields():
    player = Player(
        name="Iron Man", 
        universe_id=Universe(name="Marvel", description="A universe of superheroes").id,
        height=180.0,
        weight=80.0
    )
    assert player.name == "Iron Man"
    assert player.height == 180.0
    assert player.weight == 80.0

    for field, field_type in PLAYER_FIELDS.items():
        assert isinstance(getattr(player, field), field_type)
