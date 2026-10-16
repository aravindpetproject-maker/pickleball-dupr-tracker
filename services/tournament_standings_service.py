class TournamentStandingsService:

    @staticmethod
    def calculate_standings(
        tournament
    ):

        standings = {}

        tournament_type = tournament.get(
            "type",
            "Singles"
        )

        schedule = tournament.get(
            "schedule",
            []
        )

        # ==================================
        # Singles Tournament
        # ==================================

        if tournament_type == "Singles":

            for player in tournament.get(
                "players",
                []
            ):

                standings[player] = {

                    "Player": player,
                    "Wins": 0,
                    "Losses": 0,
                    "Points": 0

                }

            for match in schedule:

                winner = match.get(
                    "winner"
                )

                if not winner:
                    continue

                player1 = match.get(
                    "player1"
                )

                player2 = match.get(
                    "player2"
                )

                loser = (
                    player2
                    if winner == player1
                    else player1
                )

                standings[winner][
                    "Wins"
                ] += 1

                standings[winner][
                    "Points"
                ] += 3

                standings[loser][
                    "Losses"
                ] += 1

            return sorted(

                standings.values(),

                key=lambda row: (

                    row["Points"],
                    row["Wins"]

                ),

                reverse=True

            )

        # ==================================
        # Doubles Tournament
        # ==================================

        teams = set()

        for match in schedule:

            teams.add(
                match.get(
                    "team1"
                )
            )

            teams.add(
                match.get(
                    "team2"
                )
            )

        for team in teams:

            standings[team] = {

                "Player": team,
                "Wins": 0,
                "Losses": 0,
                "Points": 0

            }

        for match in schedule:

            winner = match.get(
                "winner"
            )

            if not winner:
                continue

            team1 = match.get(
                "team1"
            )

            team2 = match.get(
                "team2"
            )

            loser = (
                team2
                if winner == team1
                else team1
            )

            standings[winner][
                "Wins"
            ] += 1

            standings[winner][
                "Points"
            ] += 3

            standings[loser][
                "Losses"
            ] += 1

        return sorted(

            standings.values(),

            key=lambda row: (

                row["Points"],
                row["Wins"]

            ),

            reverse=True

        )