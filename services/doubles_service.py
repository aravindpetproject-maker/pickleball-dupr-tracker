from services.player_service import (
    PlayerService
)


class DoublesService:

    @staticmethod
    def update_doubles_stats(

        winning_ids,
        losing_ids

    ):

        players = (
            PlayerService.get_players()
        )

        for player in players:

            if player["id"] in winning_ids:

                player["wins"] += 1
                player["matchesPlayed"] += 1

            elif player["id"] in losing_ids:

                player["losses"] += 1
                player["matchesPlayed"] += 1

            if player["matchesPlayed"] > 0:

                player["winPercentage"] = round(

                    (
                        player["wins"]
                        /
                        player["matchesPlayed"]
                    ) * 100,

                    2

                )

        PlayerService.save_players(
            players
        )