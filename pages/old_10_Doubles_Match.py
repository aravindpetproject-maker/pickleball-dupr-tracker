import streamlit as st

from services.player_service import (
    PlayerService
)

from services.match_service import (
    MatchService
)

st.title(
    "🏓 Doubles Match"
)

players = PlayerService.get_players()

if len(players) < 4:

    st.warning(
        "At least 4 players are required."
    )

    st.stop()

player_names = [

    f"{p['id']} - "
    f"{p['firstName']} "
    f"{p['lastName']}"

    for p in players

]

st.subheader(
    "Team A"
)

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

st.subheader(
    "Team B"
)

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

selected_players = {

    team_a_player1,
    team_a_player2,
    team_b_player1,
    team_b_player2

}

if len(selected_players) != 4:

    st.error(
        "All four players must be different."
    )

    st.stop()

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
    "🏓 Save Doubles Match"
):

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

        "scoreA":
        score_a,

        "scoreB":
        score_b,

        "winner":
        winner,

        "notes":
        notes

    })

    st.success(
        "✅ Doubles Match Saved"
    )

    st.balloons()