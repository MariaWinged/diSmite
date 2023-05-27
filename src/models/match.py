from pydantic import BaseModel


class MatchPlayer(BaseModel):
    player_name: str
    god: str
    mmr: int
    tier: int

    def __str__(self):
        return f'{self.god}[{self.player_name}]: {self.mmr}'


class Team(BaseModel):
    team_number: int
    players: list[MatchPlayer]
    avg_mmr: int
    avg_tier: int

    def __str__(self):
        return f'Team {self.team_number}: {self.avg_mmr}\n' + '\n'.join(map(str, self.players))
