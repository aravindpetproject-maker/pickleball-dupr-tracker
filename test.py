from services.player_service import PlayerService

print("save_players exists:",
      hasattr(PlayerService, "save_players"))

print("update_statistics_after_match exists:",
      hasattr(PlayerService, "update_statistics_after_match"))