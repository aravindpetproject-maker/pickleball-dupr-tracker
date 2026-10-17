from services.match_service import (
    MatchService
)

from services.player_service import (
    PlayerService
)


class PartnerAnalyticsService:

    @staticmethod
    def get_partner_stats():

        matches = (
            MatchService.get_matches()
        )

        players = (
            PlayerService.get_players()
        )

        active_players = set()

        for player in players:

            active_players.add(
                f"{player['firstName']} "
                f"{player['lastName']}"
            )

            active_players.add(
                f"{player['id']} - "
                f"{player['firstName']} "
                f"{player['lastName']}"
            )

        partner_stats = {}

        for match in matches:

            if (
                match.get(
                    "matchType"
                ) != "Doubles"
            ):
                continue

            player1 = match.get(
                "teamAPlayer1",
                ""
            )

            player2 = match.get(
                "teamAPlayer2",
                ""
            )

            player3 = match.get(
                "teamBPlayer1",
                ""
            )

            player4 = match.get(
                "teamBPlayer2",
                ""
            )

            # Skip deleted players

            if (
                player1 not in active_players
                or
                player2 not in active_players
                or
                player3 not in active_players
                or
                player4 not in active_players
            ):
                continue

            team_a = sorted([
                player1,
                player2
            ])

            team_b = sorted([
                player3,
                player4
            ])

            team_a_key = (
                team_a[0],
                team_a[1]
            )

            team_b_key = (
                team_b[0],
                team_b[1]
            )

            for team_key in [
                team_a_key,
                team_b_key
            ]:

                if team_key not in partner_stats:

                    partner_stats[
                        team_key
                    ] = {

                        "matches": 0,

                        "wins": 0

                    }

                partner_stats[
                    team_key
                ]["matches"] += 1

            if (
                match.get(
                    "winner"
                )
                == "Team A"
                or
                match.get(
                    "winner"
                )
                == match.get(
                    "teamNameA"
                )
            ):

                partner_stats[
                    team_a_key
                ]["wins"] += 1

            else:

                partner_stats[
                    team_b_key
                ]["wins"] += 1

        return partner_stats