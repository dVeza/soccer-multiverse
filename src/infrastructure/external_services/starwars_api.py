import requests
import logging
from typing import List
from src.domain.entities import Player

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_starwars_players(universe_id: str) -> List[Player]:
    logger.info("Starting Star Wars character fetch")
    all_characters = []
    page = 1
    
    while True:
        try:
            url = f"https://swapi.dev/api/people/?page={page}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Fetching Star Wars batch: page={page}, count={len(data['results'])}")
            
            for character in data['results']:
                # Convert height and weight, handling potential unknown values
                try:
                    height = float(character['height']) if character['height'] != 'unknown' else 175
                    weight = float(character['mass']) if character['mass'] != 'unknown' else 75
                except ValueError:
                    height = 175  # Default height if conversion fails
                    weight = 75   # Default weight if conversion fails
                
                player = Player(
                    name=character['name'],
                    height=height,
                    weight=weight,
                    universe_id=universe_id
                )
                all_characters.append(player)
            
            if not data.get('next'):
                break
                
            page += 1
            
        except requests.RequestException as e:
            logger.error(f"Error fetching Star Wars data: {str(e)}")
            raise
    
    logger.info(f"Completed Star Wars fetch. Total players: {len(all_characters)}")
    return all_characters 