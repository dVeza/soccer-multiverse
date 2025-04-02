import requests
import logging
from typing import List
from src.domain.entities import Player

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_pokemon_players(universe_id: str) -> List[Player]:
    logger.info("Starting Pokemon player fetch")
    all_pokemon = []
    offset = 0
    limit = 100  # Pokemon API default limit
    
    while True:
        try:
            url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if not data['results']:
                break
                
            logger.info(f"Fetching Pokemon batch: offset={offset}, count={len(data['results'])}")
            
            for pokemon in data['results']:
                detail_response = requests.get(pokemon['url'])
                detail_response.raise_for_status()
                pokemon_data = detail_response.json()
                
                player = Player(
                    name=pokemon_data['name'].capitalize(),
                    height=pokemon_data['height'] * 10,  # Convert to cm
                    weight=pokemon_data['weight'] / 10,  # Convert to kg
                    universe_id=universe_id
                )
                all_pokemon.append(player)
            
            offset += limit
            if offset >= data['count']:
                break
                
        except requests.RequestException as e:
            logger.error(f"Error fetching Pokemon data: {str(e)}")
            raise
    
    logger.info(f"Completed Pokemon fetch. Total players: {len(all_pokemon)}")
    return all_pokemon 