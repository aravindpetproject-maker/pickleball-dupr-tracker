from datetime import datetime

from services.file_service import (
    load_json,
    save_json
)


class PlayerService:

    FILE_NAME = "players.json"

    @staticmethod
    def get_players():

        return load_json(
            PlayerService.FILE_NAME
        )

    @staticmethod
    def get_player_by_id(
        player_id
    ):

        players = load_json(
            PlayerService.FILE_NAME
        )

        for player in players:

            if player["id"] == player_id:

                return player

        return None

    @staticmethod
    def add_player(player):

        players = load_json(
            PlayerService.FILE_NAME
        )

        next_id = max(
            [
                p["id"]
                for p in players
            ],
            default=0
        ) + 1

        player["id"] = next_id


        player["winPercentage"] = 0





#######new code for including doubles


        player["currentDuprSingles"] = 3.5
        player["previousDuprSingles"] = 3.5

        player["currentDuprDoubles"] = 3.5
        player["previousDuprDoubles"] = 3.5

        player["matchesPlayed"] = 0
        player["wins"] = 0
        player["losses"] = 0

        player["singlesWins"] = 0
        player["singlesLosses"] = 0
        player["singlesMatchesPlayed"] = 0
        player["singlesWinPercentage"] = 0

        player["doublesWins"] = 0
        player["doublesLosses"] = 0
        player["doublesMatchesPlayed"] = 0
        player["doublesWinPercentage"] = 0





######new code for including doubles

        player["createdAt"] = str(
            datetime.now()
        )

        players.append(player)

        save_json(
            PlayerService.FILE_NAME,
            players
        )

        return player

    @staticmethod
    def update_player(
        player_id,
        updated_player
    ):

        players = load_json(
            PlayerService.FILE_NAME
        )

        for idx, player in enumerate(players):

            if player["id"] == player_id:

                players[idx].update(
                    updated_player
                )

                save_json(
                    PlayerService.FILE_NAME,
                    players
                )

                return True

        return False

    @staticmethod
    def delete_player(
        player_id
    ):

        players = load_json(
            PlayerService.FILE_NAME
        )

        players = [
            p
            for p in players
            if p["id"] != player_id
        ]

        save_json(
            PlayerService.FILE_NAME,
            players
        )

    @staticmethod
    def search_players(
        search_text
    ):

        players = load_json(
            PlayerService.FILE_NAME
        )

        if not search_text:
            return players

        search_text = (
            search_text.lower()
        )

        return [

            player

            for player in players

            if (
                search_text in player["firstName"].lower()
                or
                search_text in player["lastName"].lower()
                or
                search_text in player["email"].lower()
            )

        ]

    @staticmethod
    def save_players(
        players
    ):

        save_json(
            PlayerService.FILE_NAME,
            players
        )

    @staticmethod
    def update_statistics_after_match(
        winner_id,
        loser_id,
        match_type="Singles"
    ):

        players = load_json(
            PlayerService.FILE_NAME
        )

        for player in players:

            if player["id"] == winner_id:

                player["wins"] += 1
                player["matchesPlayed"] += 1

                if match_type == "Singles":

                    player["singlesWins"] = (
                        player.get(
                            "singlesWins",
                            0
                        ) + 1
                    )

                    player["singlesMatchesPlayed"] = (
                        player.get(
                            "singlesMatchesPlayed",
                            0
                        ) + 1
                    )

                elif match_type == "Doubles":

                    player["doublesWins"] = (
                        player.get(
                            "doublesWins",
                            0
                        ) + 1
                    )

                    player["doublesMatchesPlayed"] = (
                        player.get(
                            "doublesMatchesPlayed",
                            0
                        ) + 1
                    )

            elif player["id"] == loser_id:

                player["losses"] += 1
                player["matchesPlayed"] += 1

                if match_type == "Singles":

                    player["singlesLosses"] = (
                    player.get(
                        "singlesLosses",
                        0
                    ) + 1
                )

                    player["singlesMatchesPlayed"] = (
                    player.get(
                        "singlesMatchesPlayed",
                        0
                    ) + 1
                )

                elif match_type == "Doubles":

                    player["doublesLosses"] = (
                    player.get(
                        "doublesLosses",
                        0
                    ) + 1
                )

                    player["doublesMatchesPlayed"] = (
                    player.get(
                        "doublesMatchesPlayed",
                        0
                    ) + 1
                )

            if player["matchesPlayed"] > 0:

                player["winPercentage"] = round(
                    (
                        player["wins"]
                        /
                        player["matchesPlayed"]
                    ) * 100,
                    2
                )

            if player.get(
                "singlesMatchesPlayed",
                0
            ) > 0:

                player["singlesWinPercentage"] = round(
                    (
                        player.get(
                            "singlesWins",
                            0
                        )
                        /
                        player[
                            "singlesMatchesPlayed"
                        ]
                    ) * 100,
                    2
                )

            if player.get(
                "doublesMatchesPlayed",
                0
            ) > 0:

                player["doublesWinPercentage"] = round(
                    (
                        player.get(
                            "doublesWins",
                            0
                        )
                        /
                        player[
                            "doublesMatchesPlayed"
                        ]
                    ) * 100,
                    2
                )

        save_json(
            PlayerService.FILE_NAME,
            players
        )

        

    @staticmethod
    def get_top_players():

        players = load_json(
            PlayerService.FILE_NAME
        )

        return sorted(
            players,
            key=lambda player:
            player["previousDupr"],
            reverse=True
        )

    @staticmethod
    def get_top_win_percentage():

        players = load_json(
            PlayerService.FILE_NAME
        )

        return sorted(
            players,
            key=lambda player:
            player["winPercentage"],
            reverse=True
        )