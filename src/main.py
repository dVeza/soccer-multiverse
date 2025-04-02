from src.domain.services import TeamGeneratorService, TeamConfiguration
from fastapi import FastAPI
from src.api.routes import router
from src.infrastructure.db.database import init_db, SessionLocal
from contextlib import asynccontextmanager
from src.infrastructure.external_services.pokemon_api import fetch_pokemon_players
from src.infrastructure.external_services.starwars_api import fetch_starwars_players
from src.infrastructure.repositories.orm import SQLAlchemyPlayerRepository, SQLAlchemyUniverseRepository
from src.domain.entities import Universe

def import_initial_data():
    with SessionLocal() as session:
        universe_repo = SQLAlchemyUniverseRepository(session)
        player_repo = SQLAlchemyPlayerRepository(session)

        # Create or get Pokemon universe
        pokemon_universe = universe_repo.get_by_name("Pokemon")
        if not pokemon_universe:
            pokemon_universe = Universe(name="Pokemon", description="Pokemon universe")
            pokemon_universe = universe_repo.add(pokemon_universe)

        # Create or get Star Wars universe
        starwars_universe = universe_repo.get_by_name("Star Wars")
        if not starwars_universe:
            starwars_universe = Universe(name="Star Wars", description="Star Wars universe")
            starwars_universe = universe_repo.add(starwars_universe)

        # Check and import Pokemon players if needed
        pokemon_player_count = player_repo.count_by_universe(pokemon_universe.id)
        if pokemon_player_count == 0:
            pokemon_players = fetch_pokemon_players(pokemon_universe.id)
            for player in pokemon_players:
                player_repo.add(player)

        # Check and import Star Wars players if needed
        starwars_player_count = player_repo.count_by_universe(starwars_universe.id)
        if starwars_player_count == 0:
            starwars_players = fetch_starwars_players(starwars_universe.id)
            for player in starwars_players:
                player_repo.add(player)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    import_initial_data()
    yield

app = FastAPI(title="Super Soccer Showdown API", lifespan=lifespan)

app.include_router(router, prefix="/api/v1")

# if __name__ == "__main__":
#     universe_repository = InMemoryUniverseRepository()
#     player_repository = InMemoryPlayerRepository(universe_repository)
#     player_repository.load_players_from_api()
#     pokemon_players = player_repository.get_all_by_universe(universe_repository.get_by_name("Pokemon").id)
#     # starwars_players = player_repository.get_all_by_universe(universe_repository.get_by_name("Star Wars").id)
    
#     # Create service with repository
#     team_generator = TeamGeneratorService()
#     team = team_generator.generate_team(
#         universe_repository.get_by_name("Pokemon").id,
#         TeamConfiguration(num_defenders=2, num_attackers=2, num_members=5),
#         pokemon_players
#     )
#     print(team)