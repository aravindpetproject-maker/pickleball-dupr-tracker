from services.match_service import (
    MatchService
)


class PartnerAnalyticsService:

    @staticmethod
    def get_partner_stats():

        matches = (
            MatchService.get_matches()
        )

        partner_stats = {}

        for match in matches:

            if (
                match.get(
                    "matchType"
                ) != "Doubles"
            ):
                continue

            team_a = sorted([
                match["teamAPlayer1"],
                match["teamAPlayer2"]
            ])

            team_b = sorted([
                match["teamBPlayer1"],
                match["teamBPlayer2"]
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

                if team_key not in (
                    partner_stats
                ):

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
                match["winner"]
                == "Team A"
            ):

                partner_stats[
                    team_a_key
                ]["wins"] += 1

            else:

                partner_stats[
                    team_b_key
                ]["wins"] += 1

        return partner_stats