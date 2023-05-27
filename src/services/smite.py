from pyrez.api import SmiteAPI
from pyrez.models.Smite import Player
from pyrez.models.PlayerStatus import PlayerStatus
from pyrez.models.LiveMatch import LiveMatch
from pyrez.enumerations import Status
from pyrez.exceptions import PlayerNotFound

from core.config import settings
from models.player import SmitePlayer
from models.match import MatchPlayer, Team


def smite() -> SmiteAPI:
    with SmiteAPI(settings.hirez_config.devId, settings.hirez_config.authKey) as smite_api:
        return smite_api


def get_player_info(player_name: str) -> str:
    try:
        player: Player = smite().getPlayer(player_name)
    except PlayerNotFound:
        return f'Player {player_name} does not found'

    smite_player: SmitePlayer = SmitePlayer(
        name=player.playerName,
        region=player.playerRegion,
        hours_played=player.hoursPlayed,
        level=player.accountLevel,
        rank_stat_conquest=player.rankedConquest.rankStat,
        rank_stat_duel=player.rankedDuel.rankStat,
        rank_stat_joust=player.rankedJoust.rankStat,
    )
    return str(smite_player).replace(' ', '\n')


def get_player_math(player_name: str) -> str:
    try:
        status: PlayerStatus = smite().getPlayerStatus(smite().getPlayer(player_name).playerId)
    except PlayerNotFound:
        return f'Player {player_name} does not found'
    if status.status != Status.In_Game:
        return f'Player {player_name} is {status.statusString}'
    match: list[LiveMatch] = smite().getMatch(status.matchId, isLiveMatch=True)
    team_1 = Team(team_number=1, players=[], avg_mmr=0, avg_tier=0)
    team_2 = Team(team_number=2, players=[], avg_mmr=0, avg_tier=0)
    for player in match:
        match_player = MatchPlayer(
            player_name=player.playerName,
            god=player.godName,
            mmr=int(player['Rank_Stat']),
            tier=player.tier,
        )
        if player.taskForce == 1:
            team_1.players.append(match_player)
        else:
            team_2.players.append(match_player)
    team_1.avg_mmr = round(sum([p.mmr for p in team_1.players]) / len(team_1.players))
    team_1.avg_tier = round(sum([p.tier for p in team_1.players]) / len(team_1.players))

    team_2.avg_mmr = round(sum([p.mmr for p in team_2.players]) / len(team_2.players))
    team_2.avg_tier = round(sum([p.tier for p in team_2.players]) / len(team_2.players))

    return str(team_1) + '\n\n' + str(team_2)
