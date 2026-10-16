import streamlit as st
import pandas as pd

from services.player_service import (
    PlayerService
)

from services.security_service import (
    SecurityService
)

SecurityService.require_login()

SecurityService.show_user_menu()

from services.match_service import (
    MatchService
)

st.title(
    "⚔️ Head To Head Analysis"
)

players = PlayerService.get_players()

if len(players) < 2:

    st.warning(
        "At least 2 players are required."
    )

    st.stop()

player_names = [

    f"{p['firstName']} "
    f"{p['lastName']}"

    for p in players

]

player1 = st.selectbox(
    "Player 1",
    player_names,
    index=0
)

player2 = st.selectbox(
    "Player 2",
    player_names,
    index=1
)

if player1 == player2:

    st.warning(
        "Please select two different players."
    )

    st.stop()

matches = MatchService.get_matches()

head_to_head_matches = []

player1_wins = 0
player2_wins = 0

for match in matches:

    player_a = str(
        match.get(
            "playerA",
            ""
        )
    )

    player_b = str(
        match.get(
            "playerB",
            ""
        )
    )

    if (

        player1 in player_a
        and
        player2 in player_b

    ) or (

        player2 in player_a
        and
        player1 in player_b

    ):

        head_to_head_matches.append(
            match
        )

        winner = str(
            match.get(
                "winner",
                ""
            )
        )

        if player1 in winner:

            player1_wins += 1

        elif player2 in winner:

            player2_wins += 1

total_matches = len(
    head_to_head_matches
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Matches Played",
        total_matches
    )

with col2:

    st.metric(
        f"{player1} Wins",
        player1_wins
    )

with col3:

    st.metric(
        f"{player2} Wins",
        player2_wins
    )

if total_matches > 0:

    player1_pct = round(
        (
            player1_wins /
            total_matches
        ) * 100,
        2
    )

    player2_pct = round(
        (
            player2_wins /
            total_matches
        ) * 100,
        2
    )

    st.divider()

    st.subheader(
        "Win Percentage"
    )

    st.write(
        f"{player1}: "
        f"{player1_pct}%"
    )

    st.write(
        f"{player2}: "
        f"{player2_pct}%"
    )

    st.divider()

    st.subheader(
        "Head To Head Matches"
    )

    st.dataframe(
        pd.DataFrame(
            head_to_head_matches
        ),
        use_container_width=True
    )

else:

    st.info(
        "No matches found."
    )