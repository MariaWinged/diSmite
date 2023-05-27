from pydantic import BaseModel


class SmitePlayer(BaseModel):
    name: str
    region: str
    hours_played: int
    level: int
    rank_stat_conquest: float
    rank_stat_duel: float
    rank_stat_joust: float
