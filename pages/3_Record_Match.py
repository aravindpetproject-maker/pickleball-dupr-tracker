import streamlit as st

from services.player_service import (
    PlayerService
)

from services.security_service import (
    SecurityService
)

SecurityService.require_organizer()
SecurityService.show_user_menu()

from services.match_service import (
    MatchService
)

from services.dupr_service import (
    DuprService
)

from services.rating_service import (
    RatingService
)

from services.tournament_service import (
    TournamentService
)

st.title("🏓 Record Match")

# ====================================
# Match Type
# ====================================

match_type = st.radio(
    "Match Type",
    [
        "Singles",
        "Doubles"
    ],
    horizontal=True
)

# ====================================
# Tournament
# ====================================

is_tournament_match = st.checkbox(
    "🏆 Tournament Match"
)

selected_tournament = None
round_name = None

if is_tournament_match:

    tournaments = (
        TournamentService.get_tournaments()
    )

    if tournaments:

        selected_tournament = st.selectbox(
            "Tournament",
            [
                t["name"]
                for t in tournaments
                if t.get("type") == match_type
            ]
        )




        tournament = (
            TournamentService
            .get_tournament_by_name(
                selected_tournament
            )
        )


        if tournament.get("type") != match_type:

            st.error(
                f"Selected tournament is a "
                f"{tournament.get('type')} tournament."
            )

            st.stop()

            st.error(
                "Selected tournament is a Doubles tournament."
            )

            st.stop()

        round_name = st.selectbox(
            "Round",
            [
                "Round Robin",
                "Quarter Final",
                "Semi Final",
                "Final"
            ]
        )

# ====================================
# Success Message
# ====================================

if st.session_state.get(
    "match_saved",
    False
):

    st.success(
        "✅ Match Saved Successfully"
    )

    del st.session_state[
        "match_saved"
    ]

# ====================================
# Players
# ====================================

players = PlayerService.get_players()

if len(players) < 2:

    st.warning(
        "Please create players first."
    )

    st.stop()

player_names = [

    f"{player['id']} - "
    f"{player['firstName']} "
    f"{player['lastName']}"

    for player in players

]

# =====================================================
# SINGLES
# =====================================================

if match_type == "Singles":

# ====================================
# Tournament Scheduled Match Selector
# ====================================

    if (
        is_tournament_match
        and
        selected_tournament
    ):




        available_matches = [

            match

            for match in (
                TournamentService
                .get_unplayed_matches(
                    selected_tournament
                )
            )

            if "player1" in match

        ]

        if not available_matches:

            st.success(
                "✅ All tournament matches have been completed."
            )

            st.stop()

        match_options = [

            f"{match['player1']} vs "
            f"{match['player2']}"

            for match in available_matches

        ]

        selected_match = st.selectbox(
            "Scheduled Match",
            match_options
        )

        selected_match_data = next(

            match

            for match in available_matches

            if
            f"{match['player1']} vs "
            f"{match['player2']}"
            ==
            selected_match

        )

        player_a_name = (
            selected_match_data[
                "player1"
            ]
        )

        player_b_name = (
            selected_match_data[
                "player2"
            ]
        )

        st.info(
            f"🏓 {player_a_name} vs {player_b_name}"
        )

    else:

        player_a = st.selectbox(
            "Player A",
            player_names
        )

        player_b = st.selectbox(
            "Player B",
            player_names,
            index=1
        )

    score_a = st.number_input(
        "Player A Score",
        min_value=0,
        max_value=30,
        value=11
    )

    score_b = st.number_input(
        "Player B Score",
        min_value=0,
        max_value=30,
        value=7
    )

    notes = st.text_area(
        "Match Notes"
    )

    if st.button(
        "💾 Save Singles Match"
    ):

        if (
            is_tournament_match
            and
            selected_tournament
        ):

            if player_a_name == player_b_name:

                st.error(
                    "Players must be different."
                )

                st.stop()

        else:

            if player_a == player_b:

                st.error(
                    "Players must be different."
                )

                st.stop()

        if (
            is_tournament_match
            and
            selected_tournament
        ):

            p1 = next(
                (

                    player

                    for player in players

                    if
                    f"{player['firstName']} "
                    f"{player['lastName']}"
                    ==
                    player_a_name
                ),
                None

            )

            p2 = next(
                (

                    player

                    for player in players

                    if
                    f"{player['firstName']} "
                    f"{player['lastName']}"
                    ==
                    player_b_name
                ),
                None

            )

            if not p1 or not p2:

                st.error(
                    "Unable to locate one or more players."
                )

                st.write(
                    "Player A:",
                    player_a_name
                )

                st.write(
                    "Player B:",
                    player_b_name
                )

                st.stop()




        else:

            player_a_id = int(
                player_a.split("-")[0].strip()
            )

            player_b_id = int(
                player_b.split("-")[0].strip()
            )

            p1 = next(
                p
                for p in players
                if p["id"] == player_a_id
            )

            p2 = next(
                p
                for p in players
                if p["id"] == player_b_id
            )

            player_a_name = (
                f"{p1['firstName']} "
                f"{p1['lastName']}"
            )

            player_b_name = (
                f"{p2['firstName']} "
                f"{p2['lastName']}"
            )


        player_a_won = (
            score_a > score_b
        )

        winner = (
            player_a_name
            if player_a_won
            else player_b_name
        )

        score_difference = abs(
            score_a - score_b
        )

        old_rating_a = p1["currentDuprSingles"]
        old_rating_b = p2["currentDuprSingles"]

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

        p1["previousDuprSingles"] = old_rating_a
        p1["currentDuprSingles"] = new_rating_a

        p2["previousDuprSingles"] = old_rating_b
        p2["currentDuprSingles"] = new_rating_b





       

        RatingService.add_rating_history({

            "playerId":
            p1["id"],

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



        RatingService.add_rating_history({

    "playerId":
    p2["id"],

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

        PlayerService.save_players(
            players
        )

        winner_id = (
            p1["id"]
            if player_a_won
            else p2["id"]
        )

        loser_id = (
            p2["id"]
            if player_a_won
            else p1["id"]
        )

        PlayerService.update_statistics_after_match(
            winner_id,
            loser_id,
            "Singles"
        )

        MatchService.add_match({

            "matchType":
            "Singles",

            "playerA":
            player_a_name,

            "playerB":
            player_b_name,

            "scoreA":
            score_a,

            "scoreB":
            score_b,

            "winner":
            winner,

            "isTournamentMatch":
            is_tournament_match,

            "tournamentName":
            selected_tournament,

            "round":
            round_name,

            "notes":
            notes

        })

        if (
            is_tournament_match
            and
            selected_tournament
        ):

            TournamentService.record_match_result(

                selected_tournament,

                player_a_name,

                player_b_name,

                winner,

                score_a,

                score_b

            )

        st.session_state[
            "match_saved"
        ] = True

        st.rerun()

# =====================================================
# DOUBLES
# =====================================================

else:

    if (
        is_tournament_match
        and
        selected_tournament
    ):

        tournament = (
            TournamentService
            .get_tournament_by_name(
                selected_tournament
            )
        )



        available_matches = [

            match

            for match in tournament.get(
                "schedule",
                []
            )

            if (
                not match.get("winner")
                and
                "team1" in match
            )

        ]

        if not available_matches:

            st.warning(
                "No unplayed doubles matches found."
            )

            st.stop()

        match_options = [

            f"{match['team1']} vs {match['team2']}"

            for match in available_matches

        ]

        selected_match = st.selectbox(
            "Scheduled Match",
            match_options
        )

        selected_match_data = next(

            match

            for match in available_matches

            if
            f"{match['team1']} vs {match['team2']}"
            ==
            selected_match

        )

        team1_name = (
            selected_match_data["team1"]
        )

        team2_name = (
            selected_match_data["team2"]
        )

        team_a_player1 = (
            selected_match_data["team1Player1"]
        )

        team_a_player2 = (
            selected_match_data["team1Player2"]
        )

        team_b_player1 = (
            selected_match_data["team2Player1"]
        )

        team_b_player2 = (
            selected_match_data["team2Player2"]
        )

        st.subheader(team1_name)

        st.write(team_a_player1)
        st.write(team_a_player2)

        st.subheader(team2_name)

        st.write(team_b_player1)
        st.write(team_b_player2)

    else:

        st.subheader("Team A")

        team_a_player1 = st.selectbox(
            "Team A Player 1",
            player_names,
            key="a1"
        )

        team_a_player2 = st.selectbox(
            "Team A Player 2",
            player_names,
            key="a2"
        )

        st.subheader("Team B")

        team_b_player1 = st.selectbox(
            "Team B Player 1",
            player_names,
            key="b1"
        )

        team_b_player2 = st.selectbox(
            "Team B Player 2",
            player_names,
            key="b2"
        )

    score_a = st.number_input(
        "Team A Score",
        min_value=0,
        max_value=30,
        value=11
    )

    score_b = st.number_input(
        "Team B Score",
        min_value=0,
        max_value=30,
        value=8
    )

    notes = st.text_area(
        "Match Notes"
    )

    if st.button(
        "💾 Save Doubles Match"
    ):

        if is_tournament_match:

            p1 = next(
                (
                    p
                    for p in players
                    if f"{p['firstName']} {p['lastName']}"
                    == team_a_player1
                ),
                None
            )

            p2 = next(
                (
                    p
                    for p in players
                    if f"{p['firstName']} {p['lastName']}"
                    == team_a_player2
                ),
                None
                
            )

            p3 = next(
                (
                    p
                    for p in players
                    if f"{p['firstName']} {p['lastName']}"
                    == team_b_player1
                ),
                None
            )

            p4 = next(
                (
                    p
                    for p in players
                    if f"{p['firstName']} {p['lastName']}"
                    == team_b_player2
                ),
                None
            )

            if not all([p1, p2, p3, p4]):

                st.error(
                    "Unable to locate one or more players."
                )

                st.write("A1:", team_a_player1)
                st.write("A2:", team_a_player2)
                st.write("B1:", team_b_player1)
                st.write("B2:", team_b_player2)

                st.stop()

        else:








            player1_id = int(
                team_a_player1.split("-")[0].strip()
            )

            player2_id = int(
                team_a_player2.split("-")[0].strip()
            )

            player3_id = int(
                team_b_player1.split("-")[0].strip()
            )

            player4_id = int(
                team_b_player2.split("-")[0].strip()
            )

            p1 = next(
                p for p in players
                if p["id"] == player1_id
            )

            p2 = next(
                p for p in players
                if p["id"] == player2_id
            )   

            p3 = next(
                p for p in players
                if p["id"] == player3_id
            )

            p4 = next(
                p for p in players
                if p["id"] == player4_id
            )

        if len({
            p1["id"],
            p2["id"],
            p3["id"],
            p4["id"]
        }) < 4:

            st.error(
                "Each player may only appear once in a doubles match."
            )

            st.stop()


# ====================================
# Doubles DUPR Calculation
# ====================================

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

        team_a_won = score_a > score_b


        if team_a_won:

            winners = [p1, p2]
            losers = [p3, p4]

        else:

            winners = [p3, p4]
            losers = [p1, p2]

        for player in winners:

            player["wins"] += 1
            player["matchesPlayed"] += 1

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

        for player in losers:

            player["losses"] += 1
            player["matchesPlayed"] += 1

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

        for player in [p1, p2, p3, p4]:

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








        score_difference = abs(
            score_a - score_b
        )

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

            player["previousDuprDoubles"] = (
                player["currentDuprDoubles"]
            )

            player["currentDuprDoubles"] = round(

                player["currentDuprDoubles"]

                +

                (
                    change_team_a / 100
                ),

                3

            )

        for player in [p3, p4]:

            player["previousDuprDoubles"] = (
                player["currentDuprDoubles"]
            )

            player["currentDuprDoubles"] = round(

                player["currentDuprDoubles"]

                +

                (
                    change_team_b / 100
                ),

                3

            )




        for player in [p1, p2, p3, p4]:

            RatingService.add_rating_history({

                "playerId":
                player["id"],

                "ratingType":
                "Doubles",

                "previousRating":
                player["previousDuprDoubles"],

                "newRating":
                player["currentDuprDoubles"],

                "ratingChange":
                round(

                    player["currentDuprDoubles"]

                    -

                    player["previousDuprDoubles"],

                    3

                )

            })

        PlayerService.save_players(
            players
        )



        

        if is_tournament_match:

            winner = (
                team1_name
                if score_a > score_b
                else team2_name
            )

        else:

            winner = (
                "Team A"
                if score_a > score_b
                else "Team B"
            )

        MatchService.add_match({

            "matchType":
            "Doubles",

            "teamAPlayer1":
            team_a_player1,

            "teamAPlayer2":
            team_a_player2,

            "teamBPlayer1":
            team_b_player1,

            "teamBPlayer2":
            team_b_player2,

            "teamNameA":
            (
                team1_name
                if is_tournament_match
                else "Team A"
            ),

            "teamNameB":
            (
                team2_name
                if is_tournament_match
                else "Team B"
            ),

            "scoreA":
            score_a,

            "scoreB":
            score_b,

            "winner":
            winner,

            "isTournamentMatch":
            is_tournament_match,

            "tournamentName":
            selected_tournament,

            "round":
            round_name,

            "notes":
            notes

        })

        if (
            is_tournament_match
            and
            selected_tournament
        ):

            winner_team = (
                team1_name
                if score_a > score_b
                else team2_name
            )

            TournamentService.record_doubles_match_result(

                selected_tournament,

                team1_name,

                team2_name,

                winner_team,

                score_a,

                score_b

            )


            st.cache_data.clear()
            st.cache_resource.clear()

        st.session_state[
            "match_saved"
        ] = True

        st.session_state[
        "refresh_tournament"
        ] = True



        st.rerun()