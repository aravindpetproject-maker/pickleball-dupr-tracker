from services.file_service import (
    load_json,
    save_json
)

from services.dupr_service import (
    DuprService
)


class RecalculationService:

    @staticmethod
    def recalculate_all():

        players = load_json(
            "players.json"
        )

        matches = load_json(
            "matches.json"
        )

        # ==================================
        # Reset Players
        # ==================================

        for player in players:

            player.setdefault(
                "previousDuprSingles",
                3.5
            )

            player.setdefault(
                "currentDuprSingles",
                3.5
            )

            player.setdefault(
                "previousDuprDoubles",
                3.5
            )

            player.setdefault(
                "currentDuprDoubles",
                3.5
            )

            player["previousDuprSingles"] = 3.5
            player["currentDuprSingles"] = 3.5

            player["previousDuprDoubles"] = 3.5
            player["currentDuprDoubles"] = 3.5

            player["wins"] = 0
            player["losses"] = 0

            player["matchesPlayed"] = 0
            player["winPercentage"] = 0

            player["singlesWins"] = 0
            player["singlesLosses"] = 0
            player["singlesMatchesPlayed"] = 0
            player["singlesWinPercentage"] = 0

            player["doublesWins"] = 0
            player["doublesLosses"] = 0
            player["doublesMatchesPlayed"] = 0
            player["doublesWinPercentage"] = 0

        ratings = []

        matches = sorted(
            matches,
            key=lambda x: x.get(
                "id",
                0
            )
        )

        # ==================================
        # Replay Matches
        # ==================================

        for match in matches:

            match_type = match.get(
                "matchType"
            )

            # ==================================
            # SINGLES
            # ==================================

            if match_type == "Singles":

                player_a = match.get(
                    "playerA"
                )

                player_b = match.get(
                    "playerB"
                )

                if not player_a or not player_b:
                    continue

                p1 = next(
                    (
                        p
                        for p in players
                        if (
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            == player_a
                            or
                            f"{p['id']} - "
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            == player_a
                        )
                    ),
                    None
                )

                p2 = next(
                    (
                        p
                        for p in players
                        if (
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            == player_b
                            or
                            f"{p['id']} - "
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            == player_b
                        )
                    ),
                    None
                )

                if not p1 or not p2:
                    continue

                score_a = int(
                    match.get(
                        "scoreA",
                        0
                    )
                )

                score_b = int(
                    match.get(
                        "scoreB",
                        0
                    )
                )

                player_a_won = (
                    score_a > score_b
                )

                score_difference = abs(
                    score_a - score_b
                )

                old_rating_a = (
                    p1[
                        "currentDuprSingles"
                    ]
                )

                old_rating_b = (
                    p2[
                        "currentDuprSingles"
                    ]
                )

                change_a = (
                    DuprService.calculate_rating_change(
                        old_rating_a,
                        old_rating_b,
                        player_a_won,
                        score_difference
                    )
                )

                change_b = (
                    DuprService.calculate_rating_change(
                        old_rating_b,
                        old_rating_a,
                        not player_a_won,
                        score_difference
                    )
                )

                new_rating_a = round(
                    old_rating_a +
                    (change_a / 100),
                    3
                )

                new_rating_b = round(
                    old_rating_b +
                    (change_b / 100),
                    3
                )

                p1[
                    "previousDuprSingles"
                ] = old_rating_a

                p2[
                    "previousDuprSingles"
                ] = old_rating_b

                p1[
                    "currentDuprSingles"
                ] = new_rating_a

                p2[
                    "currentDuprSingles"
                ] = new_rating_b

                p1["matchesPlayed"] += 1
                p2["matchesPlayed"] += 1

                p1["singlesMatchesPlayed"] += 1
                p2["singlesMatchesPlayed"] += 1

                if player_a_won:

                    p1["wins"] += 1
                    p1["singlesWins"] += 1

                    p2["losses"] += 1
                    p2["singlesLosses"] += 1

                else:

                    p2["wins"] += 1
                    p2["singlesWins"] += 1

                    p1["losses"] += 1
                    p1["singlesLosses"] += 1


                ratings.append({

                    "id":
                    len(ratings) + 1,

                    "playerId":
                    p1["id"],

                    "matchId":
                    match["id"],

                    "ratingType":
                    "Singles",

                    "previousRating":
                    old_rating_a,

                    "newRating":
                    new_rating_a,

                    "ratingChange":
                    round(
                        new_rating_a -
                        old_rating_a,
                        3
                    )
                })

                ratings.append({

                    "id":
                    len(ratings) + 1,

                    "playerId":
                    p2["id"],

                    "matchId":
                    match["id"],

                    "ratingType":
                    "Singles",

                    "previousRating":
                    old_rating_b,

                    "newRating":
                    new_rating_b,

                    "ratingChange":
                    round(
                        new_rating_b -
                        old_rating_b,
                        3
                    )
                })

            # ==================================
            # DOUBLES
            # ==================================

            elif match_type == "Doubles":

                p1 = next(
                    (
                        p
                        for p in players
                        if (
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            ==
                            match.get(
                                "teamAPlayer1"
                            )
                            or
                            f"{p['id']} - "
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            ==
                            match.get(
                                "teamAPlayer1"
                            )
                        )
                    ),
                    None
                )

                p2 = next(
                    (
                        p
                        for p in players
                        if (
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            ==
                            match.get(
                                "teamAPlayer2"
                            )
                            or
                            f"{p['id']} - "
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            ==
                            match.get(
                                "teamAPlayer2"
                            )
                        )
                    ),
                    None
                )

                p3 = next(
                    (
                        p
                        for p in players
                        if (
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            ==
                            match.get(
                                "teamBPlayer1"
                            )
                            or
                            f"{p['id']} - "
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            ==
                            match.get(
                                "teamBPlayer1"
                            )
                        )
                    ),
                    None
                )

                p4 = next(
                    (
                        p
                        for p in players
                        if (
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            ==
                            match.get(
                                "teamBPlayer2"
                            )
                            or
                            f"{p['id']} - "
                            f"{p['firstName']} "
                            f"{p['lastName']}"
                            ==
                            match.get(
                                "teamBPlayer2"
                            )
                        )
                    ),
                    None
                )

                if not all(
                    [p1, p2, p3, p4]
                ):
                    continue

                score_a = int(
                    match.get(
                        "scoreA",
                        0
                    )
                )

                score_b = int(
                    match.get(
                        "scoreB",
                        0
                    )
                )

                team_a_won = (
                    score_a > score_b
                )

                score_difference = abs(
                    score_a - score_b
                )

                team_a_rating = (
                    p1["currentDuprDoubles"]
                    +
                    p2["currentDuprDoubles"]
                ) / 2

                team_b_rating = (
                    p3["currentDuprDoubles"]
                    +
                    p4["currentDuprDoubles"]
                ) / 2

                change_team_a = (
                    DuprService.calculate_rating_change(
                        team_a_rating,
                        team_b_rating,
                        team_a_won,
                        score_difference
                    )
                )

                change_team_b = (
                    DuprService.calculate_rating_change(
                        team_b_rating,
                        team_a_rating,
                        not team_a_won,
                        score_difference
                    )
                )

                for player in [p1, p2]:

                    old_rating = (
                        player[
                            "currentDuprDoubles"
                        ]
                    )

                    player[
                        "previousDuprDoubles"
                    ] = old_rating

                    player[
                        "currentDuprDoubles"
                    ] = round(
                        old_rating +
                        (
                            change_team_a
                            / 100
                        ),
                        3
                    )

                    ratings.append({

                        "id":
                        len(ratings) + 1,

                        "playerId":
                        player["id"],

                        "matchId":
                        match["id"],

                        "ratingType":
                        "Doubles",

                        "previousRating":
                        old_rating,

                        "newRating":
                        player[
                            "currentDuprDoubles"
                        ],

                        "ratingChange":
                        round(
                            player[
                                "currentDuprDoubles"
                            ] -
                            old_rating,
                            3
                        )
                    })

                for player in [p3, p4]:

                    old_rating = (
                        player[
                            "currentDuprDoubles"
                        ]
                    )

                    player[
                        "previousDuprDoubles"
                    ] = old_rating

                    player[
                        "currentDuprDoubles"
                    ] = round(
                        old_rating +
                        (
                            change_team_b
                            / 100
                        ),
                        3
                    )

                    ratings.append({

                        "id":
                        len(ratings) + 1,

                        "playerId":
                        player["id"],

                        "matchId":
                        match["id"],

                        "ratingType":
                        "Doubles",

                        "previousRating":
                        old_rating,

                        "newRating":
                        player[
                            "currentDuprDoubles"
                        ],

                        "ratingChange":
                        round(
                            player[
                                "currentDuprDoubles"
                            ] -
                            old_rating,
                            3
                        )
                    })

                winners = (
                    [p1, p2]
                    if team_a_won
                    else [p3, p4]
                )

                losers = (
                    [p3, p4]
                    if team_a_won
                    else [p1, p2]
                )

                for player in winners:

                    player["wins"] += 1
                    player["matchesPlayed"] += 1

                    player["doublesWins"] += 1
                    player["doublesMatchesPlayed"] += 1

                for player in losers:

                    player["losses"] += 1
                    player["matchesPlayed"] += 1

                    player["doublesLosses"] += 1
                    player["doublesMatchesPlayed"] += 1

        # ==================================
        # Win Percentage
        # ==================================

        for player in players:

            if (
                player[
                    "matchesPlayed"
                ] > 0
            ):

                player[
                    "winPercentage"
                ] = round(
                    (
                        player["wins"]
                        /
                        player[
                            "matchesPlayed"
                        ]
                    ) * 100,
                    2
                )

                if player["singlesMatchesPlayed"] > 0:

                    player["singlesWinPercentage"] = round(
                        (
                            player["singlesWins"]
                            /
                            player["singlesMatchesPlayed"]
                        ) * 100,
                        2
                    )

                if player["doublesMatchesPlayed"] > 0:

                    player["doublesWinPercentage"] = round(
                        (
                            player["doublesWins"]
                            /
                            player["doublesMatchesPlayed"]
                        ) * 100,
                        2
                    )

        # ==================================
        # Save
        # ==================================

        print("========== RECALC RESULTS ==========")

        for player in players:

            print(
                player["firstName"],
                player["lastName"],
                "Singles:",
                player["currentDuprSingles"],
                "Doubles:",
                player["currentDuprDoubles"]
                )




        save_json(
            "players.json",
            players
        )

        save_json(
            "ratings.json",
            ratings
        )

        save_json(
            "statistics.json",
            []
        )

        return {

            "players":
            len(players),

            "matches":
            len(matches),

            "ratings":
            len(ratings)
        }