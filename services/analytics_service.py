from services.file_service import (
    load_json
)


class AnalyticsService:

    @staticmethod
    def get_leaderboard():

        players = load_json(
            "players.json"
        )

        return sorted(
            players,
            key=lambda player:
            player["currentDupr"],
            reverse=True
        )

    @staticmethod
    def get_top_win_percentage():

        players = load_json(
            "players.json"
        )

        return sorted(
            players,
            key=lambda player:
            player["winPercentage"],
            reverse=True
        )

    @staticmethod
    def get_top_improved():

        ratings = load_json(
            "ratings.json"
        )

        improvements = {}

        for rating in ratings:

            player_id = (
                rating["playerId"]
            )

            improvements[player_id] = (
                improvements.get(
                    player_id,
                    0
                )
                +
                rating["ratingChange"]
            )

        return sorted(
            improvements.items(),
            key=lambda item:
            item[1],
            reverse=True
        )
       
       
    @staticmethod
    def get_match_type_counts():

        matches = load_json(
            "matches.json"
        )

        singles = 0
        doubles = 0

        for match in matches:

            if (
                match.get(
                    "matchType"
                )
                == "Singles"
            ):

                singles += 1

            elif (
                match.get(
                    "matchType"
                )
                == "Doubles"
            ):

                doubles += 1

        return {

            "singles":
            singles,

            "doubles":
            doubles

        }

    @staticmethod
    def get_most_improved_players():

        players = load_json(
            "players.json"
        )

        ratings = load_json(
            "ratings.json"
        )

        improvements = {}

        for rating in ratings:

            player_id = rating[
                "playerId"
            ]

            improvements[
                player_id
            ] = improvements.get(
                player_id,
                0
            ) + rating[
                "ratingChange"
            ]

        result = []

        for player in players:

            improvement = round(

                improvements.get(
                    player["id"],
                    0
                ),

                3

            )

            result.append({

                "Player":
                f"{player['firstName']} "
                f"{player['lastName']}",

                "Improvement":
                improvement

            })

        return sorted(

            result,

            key=lambda x:
            x["Improvement"],

            reverse=True

        )