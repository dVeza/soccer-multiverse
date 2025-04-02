from src.domain.entities import Position, Team, Player
from typing import List
import uuid
from dataclasses import dataclass


class InvalidTeamConfigurationError(Exception):
    pass


@dataclass
class TeamConfiguration:
    defenders: int
    attackers: int
    total_players: int = 5  # Always 5 players (4 field + 1 goalie)
    
    def validate(self):
        if self.defenders + self.attackers != 4:
            raise InvalidTeamConfigurationError(
                "Team must have exactly 4 field players (defenders + attackers)"
            )
        if self.defenders > 4:
            raise InvalidTeamConfigurationError("Maximum 4 defenders allowed")
        if self.attackers > 4:
            raise InvalidTeamConfigurationError("Maximum 4 attackers allowed")
        if self.total_players != 5:
            raise InvalidTeamConfigurationError("Team must have exactly 5 players")


class TeamGeneratorService:
    def generate_team(
        self,
        universe_id: str,
        config: TeamConfiguration,
        available_players: List[Player],
    ) -> Team:
        # Validate configuration before proceeding
        config.validate()

        team = Team(name=f"Team {uuid.uuid4().hex[:6]}", universe_id=universe_id)

        # Assign goalie (tallest player)
        goalie = max(available_players, key=lambda p: p.height)
        team.add_player(goalie, Position.GOALIE)
        available_players.remove(goalie)

        # Assign defenders (heaviest players)
        defenders = sorted(available_players, key=lambda p: p.weight, reverse=True)
        for defender in defenders[: config.defenders]:
            team.add_player(defender, Position.DEFENCE)
            available_players.remove(defender)

        # Assign attackers (shortest remaining players)
        attackers = sorted(available_players, key=lambda p: p.height)
        for attacker in attackers[: config.attackers]:
            team.add_player(attacker, Position.OFFENCE)
            available_players.remove(attacker)

        return team
