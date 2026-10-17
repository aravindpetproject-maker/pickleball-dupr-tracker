import streamlit as st

from services.player_service import (
    PlayerService
)

from services.match_service import (
    MatchService
)

from services.security_service import (
    SecurityService
)

from services.recalculation_service import (
    RecalculationService
)

from services.file_service import (
    load_json,
    save_json
)

SecurityService.require_admin()

SecurityService.show_user_menu()

st.title(
    "🧹 Data Management"
)

st.warning(
    "Admin Only Feature"
)

# =====================================
# Success Messages
# =====================================

if (
    "player_delete_message"
    in st.session_state
):

    st.success(
        st.session_state[
            "player_delete_message"
        ]
    )

    del st.session_state[
        "player_delete_message"
    ]


if (
    "tournament_delete_message"
    in st.session_state
):

    st.success(
        st.session_state[
            "tournament_delete_message"
        ]
    )

    del st.session_state[
        "tournament_delete_message"
    ]

if (
    "tournament_delete_message"
    in st.session_state
):

    st.success(
        st.session_state[
            "tournament_delete_message"
        ]
    )

    del st.session_state[
        "tournament_delete_message"
    ]

players = PlayerService.get_players()

search_text = st.text_input(
    "Search Player Name"
)

matching_players = []

for player in players:

    full_name = (
        f"{player.get('firstName', '')} "
        f"{player.get('lastName', '')}"
    )

    if (
        not search_text
        or
        search_text.lower()
        in full_name.lower()
    ):

        matching_players.append(
            player
        )

if matching_players:

    player_options = {

        f"{player['firstName']} "
        f"{player['lastName']}": player

        for player in matching_players

    }

    selected_name = st.selectbox(
        "Select Player",
        list(player_options.keys())
    )

    selected_player = player_options[
        selected_name
    ]

    player_name = (
        f"{selected_player['firstName']} "
        f"{selected_player['lastName']}"
    )

    ##st.subheader(
      #  "Player Details"
    #)

    #st.json(
     #   selected_player
    #)

    matches = load_json(
        "matches.json"
    )

    ratings = load_json(
        "ratings.json"
    )

    match_count = 0

    for match in matches:

        if (
            player_name.lower()
            in str(match).lower()
        ):
            match_count += 1

    rating_count = len(
        [
            rating
            for rating in ratings
            if rating.get(
                "playerId"
            )
            ==
            selected_player["id"]
        ]
    )

    st.info(
        f"""
Player: {player_name}

Matches Found: {match_count}

Rating Records: {rating_count}
"""
    )

    st.divider()

    confirm_delete = st.checkbox(
        "I understand this action cannot be undone"
    )

    col1, col2 = st.columns(2)

    #
    # Delete Player Only
    #

    with col1:

        if st.button(
            "🗑 Delete Player Only"
        ):

            if not confirm_delete:

                st.warning(
                    "Please confirm deletion."
                )

                st.stop()

            remaining_players = [

                player

                for player in players

                if player["id"]
                !=
                selected_player["id"]

            ]

            save_json(
                "players.json",
                remaining_players
            )

# =====================================
# Remove Player From Tournaments
# =====================================

            tournaments = load_json(
                "tournaments.json"
            )

            for tournament in tournaments:

                # Remove from player list

                tournament["players"] = [

                    player

                    for player in tournament.get(
                        "players",
                        []
                    )

                    if player != player_name

                ]

            # Remove any doubles teams containing player

                updated_teams = []

                for team in tournament.get(
                    "teams",
                    []
                ):

                    if (
                        team.get("player1") == player_name
                        or
                        team.get("player2") == player_name
                    ):

                        continue

                    updated_teams.append(
                        team
                    )

                tournament["teams"] = updated_teams

    # Remove scheduled matches containing player

                updated_schedule = []

                for match in tournament.get(
                    "schedule",
                    []
                ):

                    remove_match = False

        # Singles

                    if (
                        player_name
                        in [
                            match.get("player1"),
                            match.get("player2")
                        ]
                    ):

                        remove_match = True

        # Doubles

                    if (
                        player_name
                        in [
                            match.get("team1Player1"),
                            match.get("team1Player2"),
                            match.get("team2Player1"),
                            match.get("team2Player2")
                        ]
                    ):

                        remove_match = True

                    if not remove_match:

                        updated_schedule.append(
                            match
                        )

                tournament["schedule"] = (
                    updated_schedule
                )

            save_json(
                "tournaments.json",
                tournaments
            )

            st.session_state[
                "player_delete_message"
            ] = (
                f"✅ Player '{player_name}' removed from Players and Tournaments."
            )



            st.rerun()

    #
    # Delete Player + History
    #

    with col2:

        if st.button(
            "☢ Delete Player + History"
        ):

            if not confirm_delete:

                st.warning(
                    "Please confirm deletion."
                )

                st.stop()

            player_id = selected_player[
                "id"
            ]

            #
            # Remove Player
            #

            remaining_players = [

                player

                for player in players

                if player["id"]
                !=
                player_id

            ]

            save_json(
                "players.json",
                remaining_players
            )

            #
            # Remove 

                    # =====================================
            # Remove Player From Tournaments
            # =====================================

            tournaments = load_json(
                "tournaments.json"
            )

            for tournament in tournaments:

                tournament["players"] = [

                    player

                    for player in tournament.get(
                        "players",
                        []
                    )

                    if player != player_name

                ]

                updated_teams = []

                for team in tournament.get(
                    "teams",
                    []
                ):

                    if (
                        team.get("player1") == player_name
                        or
                        team.get("player2") == player_name
                    ):

                        continue

                    updated_teams.append(
                        team
                    )

                tournament["teams"] = (
                    updated_teams
                )

                updated_schedule = []

                for match in tournament.get(
                    "schedule",
                    []
                ):

                    remove_match = False

                    participants = [

                        match.get("player1", ""),

                        match.get("player2", ""),

                        match.get("team1Player1", ""),

                        match.get("team1Player2", ""),

                        match.get("team2Player1", ""),

                        match.get("team2Player2", "")

                    ]

                    for participant in participants:

                        if (
                            participant == player_name
                            or
                            participant.endswith(
                                f" - {player_name}"
                            )
                        ):

                            remove_match = True
                            break

                        

                    if player_name in [

                        match.get(
                            "team1Player1"
                        ),

                        match.get(
                            "team1Player2"
                        ),

                        match.get(
                            "team2Player1"
                        ),

                        match.get(
                            "team2Player2"
                        )

                    ]:

                        remove_match = True

                    if not remove_match:

                        updated_schedule.append(
                            match
                        )

                tournament["schedule"] = (
                    updated_schedule
                )

            save_json(
                "tournaments.json",
                tournaments
            )

            # =====================================
            # Remove Rating History
            # =====================================

            remaining_ratings = [

                rating

                for rating in ratings

                if rating.get(
                    "playerId"
                ) != player_id

            ]

            save_json(
                "ratings.json",
                remaining_ratings
            )

            # =====================================
            # Remove Match History
            # =====================================

            remaining_matches = []

            for match in matches:

                remove_match = False

                values_to_check = [

                    match.get("playerA", ""),

                    match.get("playerB", ""),

                    match.get("teamAPlayer1", ""),

                    match.get("teamAPlayer2", ""),

                    match.get("teamBPlayer1", ""),

                    match.get("teamBPlayer2", "")

                ]

                for value in values_to_check:

                    if (
                        value == player_name
                        or
                        value.endswith(
                            f" - {player_name}"
                        )
                    ):

                        remove_match = True
                        break

                if not remove_match:

                    remaining_matches.append(
                        match
                    )

            save_json(
                "matches.json",
                remaining_matches
            )

            # =====================================
            # Recalculate Ratings
            # =====================================

            RecalculationService.recalculate_all()

            st.session_state[
                "player_delete_message"
            ] = (
                f"✅ Player '{player_name}' and all related "
                f"Matches, Ratings and Tournament References "
                f"were successfully removed."
            )

            st.rerun()

# =====================================
# Tournament Management
# =====================================


st.divider()

st.subheader(
    "🏆 Tournament Management"
)

tournaments = load_json(
    "tournaments.json"
)

if tournaments:

    tournament_names = [
        tournament["name"]
        for tournament in tournaments
    ]

    selected_tournament = st.selectbox(
        "Select Tournament To Delete",
        tournament_names
    )

    confirm_tournament_delete = st.checkbox(
        "I understand tournament deletion cannot be undone"
    )

    if st.button(
        "🗑 Delete Tournament"
    ):

        if not confirm_tournament_delete:

            st.warning(
                "Please confirm deletion."
            )

            st.stop()

        remaining_tournaments = [

            tournament

            for tournament in tournaments

            if tournament["name"]
            != selected_tournament

        ]

        save_json(
            "tournaments.json",
            remaining_tournaments
        )

        st.session_state[
            "tournament_delete_message"
        ] = (
            f"✅ Tournament '{selected_tournament}' deleted successfully and removed from Tournament Manager."
        )

        st.rerun()

else:

    st.info(
        "No tournaments available."
    )