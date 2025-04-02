from typing import List, Optional
import requests
import logging
from src.domain.repositories import PlayerRepository, UniverseRepository
from src.domain.entities import Player, Universe
import random
from uuid import UUID


class InMemoryUniverseRepository(UniverseRepository):
    def __init__(self):
        self._universes = {}
        self._universes_by_name = {}
        
        # Initialize default universes
        self.pokemon_universe = Universe("Pokemon", "Pokemon Universe")
        self.starwars_universe = Universe("Star Wars", "Star Wars Universe")
        
        self.add(self.pokemon_universe)
        self.add(self.starwars_universe)
    
    def add(self, universe: Universe) -> Universe:
        self._universes[universe.id] = universe
        self._universes_by_name[universe.name.lower()] = universe
        return universe
    
    def get_by_id(self, id: UUID) -> Optional[Universe]:
        return self._universes.get(id)
    
    def get_by_name(self, name: str) -> Optional[Universe]:
        return self._universes_by_name.get(name.lower())
    
    def list(self) -> List[Universe]:
        return list(self._universes.values())


class InMemoryPlayerRepository(PlayerRepository):
    def __init__(self, universe_repository: UniverseRepository):
        self._players_by_universe = {}
        self._universe_repository = universe_repository
    
    def get_by_id(self, id: str) -> Player | None:
        for players in self._players_by_universe.values():
            player = next((p for p in players if p.id == id), None)
            if player:
                return player
        return None
    
    def list(self) -> List[Player]:
        return [p for players in self._players_by_universe.values() for p in players]
    
    def add(self, player: Player) -> Player:
        if player.universe_id not in self._players_by_universe:
            self._players_by_universe[player.universe_id] = []
        self._players_by_universe[player.universe_id].append(player)
        return player
    
    def get_all_by_universe(self, universe_id: str) -> List[Player]:
        return self._players_by_universe.get(universe_id, [])
    
    def get_random_by_universe(self, universe_id: str, count: int) -> List[Player]:
        players = self.get_all_by_universe(universe_id)
        if len(players) < count:
            raise ValueError(f"Not enough players in universe {universe_id}")
        return random.sample(players, count)

    def load_players_from_api(self):
        self._load_pokemon_data()
        # self._load_starwars_data()
    
    def _load_pokemon_data(self):
        try:
            pokemon_universe = self._universe_repository.get_by_name("pokemon")
            if not pokemon_universe:
                raise ValueError("Pokemon universe not found")
            
            response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=20")
            data = response.json()
            print(data)
            
            for pokemon in data['results']:
                details = requests.get(pokemon['url']).json()
                player = Player(
                    name=details['name'].capitalize(),
                    height=float(details['height'] * 10),
                    weight=float(details['weight'] / 10),
                    universe_id=pokemon_universe.id
                )
                self.add(player)
        except Exception as e:
            logging.error(f"Failed to load Pokemon data: {e}")
            raise

    def _load_starwars_data(self):
        try:
            response = requests.get("https://swapi.dev/api/people")
            data = response.json()
            
            for character in data['results']:
                try:
                    height = float(character['height'])
                    weight = float(character['mass'])
                except ValueError:
                    continue  # Skip characters with unknown height/weight
                
                player = Player(
                    name=character['name'],
                    height=height,
                    weight=weight,
                    universe_id="starwars"
                )
                self._players_by_universe["starwars"].append(player)
        except Exception as e:
            logging.error(f"Failed to load Star Wars data: {e}")
            raise 