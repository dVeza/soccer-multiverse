import asyncio
from ..infrastructure.services.character_sync_service import CharacterSyncService
# ... other imports ...

async def sync_all_universes():
    # Setup dependencies
    player_repository = SQLAlchemyPlayerRepository(session)
    pokemon_provider = PokemonAPI()
    starwars_provider = StarWarsAPI()
    
    sync_service = CharacterSyncService(
        player_repository,
        pokemon_provider,
        starwars_provider
    )
    
    # Sync each universe
    await sync_service.sync_universe("pokemon")
    await sync_service.sync_universe("starwars")

if __name__ == "__main__":
    asyncio.run(sync_all_universes()) 