import pytest
from uuid import UUID
from src.domain.repositories import TeamRepository, UniverseRepository, PlayerRepository
from src.domain.entities import Team, Universe, Player

class MockTeamRepository(TeamRepository):
    def __init__(self):
        self.teams = {}
        
    def get_by_id(self, id: str):
        return self.teams.get(id)
    
    def list(self):
        return list(self.teams.values())
    
    def add(self, entity: Team):
        self.teams[str(entity.id)] = entity
        return entity
        
    def get_by_universe(self, universe: str):
        return [team for team in self.teams.values() if team.universe == universe]

class MockUniverseRepository(UniverseRepository):
    def __init__(self):
        self.universes = {}
        
    def get_by_id(self, id: UUID):
        return self.universes.get(str(id))
    
    def get_by_name(self, name: str):
        return next((u for u in self.universes.values() if u.name == name), None)
    
    def list(self):
        return list(self.universes.values())
    
    def add(self, universe: Universe):
        self.universes[str(universe.id)] = universe
        return universe

# def test_team_repository():
#     repo = MockTeamRepository()
#     team = Team(id=UUID("12345678-1234-5678-1234-567812345678"), 
#                 name="Test Team", 
#                 universe=UUID("12345678-1234-5678-1234-567812345678"),
#                 players=[])
    
#     # Test add and get_by_id
#     added_team = repo.add(team)
#     assert repo.get_by_id(str(team.id)) == team
    
#     # Test list
#     assert repo.list() == [team]
    
#     # Test get_by_universe
#     assert repo.get_by_universe("star-wars") == [team]
#     assert repo.get_by_universe("pokemon") == []

def test_universe_repository():
    repo = MockUniverseRepository()
    universe = Universe(id=UUID("12345678-1234-5678-1234-567812345678"), 
                       name="Star Wars",
                       description="Star Wars universe")
    
    # Test add and get_by_id
    added_universe = repo.add(universe)
    assert repo.get_by_id(universe.id) == universe
    
    # Test get_by_name
    assert repo.get_by_name("Star Wars") == universe
    assert repo.get_by_name("Pokemon") is None
    
    # Test list
    assert repo.list() == [universe] 