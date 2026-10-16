from services.player_service import PlayerService

PlayerService.update_statistics_after_match(
    1,
    2
)

print(
    PlayerService.get_players()
)
