from datetime import datetime

from services.file_service import (
    load_json,
    save_json
)


class TournamentService:

    FILE_NAME = "tournaments.json"

    @staticmethod
    def get_tournaments():

        return load_json(
            TournamentService.FILE_NAME
        )

    @staticmethod
    def add_tournament(
        tournament
    ):

        tournaments = load_json(
            TournamentService.FILE_NAME
        )

        tournament["id"] = max(

            [
                t["id"]
                for t in tournaments
            ],

            default=0

        ) + 1

        tournament["createdAt"] = str(
            datetime.now()
        )

        tournaments.append(
            tournament
        )

        save_json(
            TournamentService.FILE_NAME,
            tournaments
        )

        return tournament

    @staticmethod
    def update_tournament(
        tournament_id,
        updated_data
    ):

        tournaments = load_json(
            TournamentService.FILE_NAME
        )

        for idx, tournament in enumerate(
            tournaments
        ):

            if (
                tournament["id"]
                == tournament_id
            ):

                tournaments[idx].update(
                    updated_data
                )

                save_json(

                    TournamentService.FILE_NAME,

                    tournaments

                )

                return True

        return False


    @staticmethod
    def delete_tournament(
        tournament_id
    ):

        tournaments = load_json(
            TournamentService.FILE_NAME
        )

        tournaments = [

            tournament

            for tournament in tournaments

            if tournament["id"]
            != tournament_id

        ]

        save_json(
            TournamentService.FILE_NAME,
            tournaments
        )

        return True

    @staticmethod
    def get_tournament_by_name(
        tournament_name
    ):

        tournaments = load_json(
            TournamentService.FILE_NAME
        )

        for tournament in tournaments:

            if (
                tournament["name"]
                == tournament_name
            ):

                return tournament

        return None

    @staticmethod
    def get_unplayed_matches(
        tournament_name
    ):

        tournaments = load_json(
            TournamentService.FILE_NAME
        )

        for tournament in tournaments:

            if (
                tournament["name"]
                == tournament_name
            ):

                return [

                    match

                    for match

                    in tournament.get(
                        "schedule",
                        []
                    )

                    if not match.get(
                        "winner"
                    )

                ]

        return []

    # ===================================
    # Singles Tournament Result
    # ===================================

    @staticmethod
    def record_match_result(

        tournament_name,

        player1,

        player2,

        winner,

        score_a,

        score_b

    ):

        tournaments = load_json(
            TournamentService.FILE_NAME
        )

        updated = False

        for tournament in tournaments:

            if (
                tournament["name"]
                !=
                tournament_name
            ):
                continue

            for match in tournament.get(
                "schedule",
                []
            ):

                p1 = match.get(
                    "player1",
                    ""
                )

                p2 = match.get(
                    "player2",
                    ""
                )

                if (
                    {p1, p2}
                    ==
                    {player1, player2}
                ):

                    match["winner"] = winner

                    match["completed"] = True

                    if p1 == player1:

                        match[
                            "scorePlayer1"
                        ] = score_a

                        match[
                            "scorePlayer2"
                        ] = score_b

                    else:

                        match[
                            "scorePlayer1"
                        ] = score_b

                        match[
                            "scorePlayer2"
                        ] = score_a

                    updated = True

                    break

        if updated:


            remaining_matches = [

                match

                for match in tournament["schedule"]

                if not match.get("winner")

            ]

            if len(remaining_matches) == 0:

                tournament["status"] = "Completed"

                tournament["champion"] = winner

            save_json(

                TournamentService.FILE_NAME,

                tournaments

            )

        return updated

    # ===================================
    # Doubles Tournament Result
    # ===================================

    @staticmethod
    def record_doubles_match_result(

        tournament_name,

        team1,

        team2,

        winner,

        score_team1,

        score_team2

    ):

        tournaments = load_json(
            TournamentService.FILE_NAME
        )

        updated = False

        for tournament in tournaments:

            if (
                tournament["name"]
                !=
                tournament_name
            ):
                continue

            for match in tournament.get(
                "schedule",
                []
            ):

                if (

                    match.get("team1")
                    ==
                    team1

                    and

                    match.get("team2")
                    ==
                    team2

                ):

                    match["winner"] = winner

                    match["completed"] = True

                    match[
                        "scoreTeam1"
                    ] = score_team1

                    match[
                        "scoreTeam2"
                    ] = score_team2

                    updated = True

                    break

        if updated:


            remaining_matches = [

                match

                for match in tournament["schedule"]

                if not match.get("winner")

            ]

            if len(remaining_matches) == 0:

                tournament["status"] = "Completed"

                tournament["champion"] = winner

            save_json(

                TournamentService.FILE_NAME,

                tournaments

            )

        return updated