import streamlit as st
import pandas as pd
import plotly.express as px

from services.player_service import (
    PlayerService
)

from services.rating_service import (
    RatingService
)

from services.security_service import (
    SecurityService
)

SecurityService.require_login()

SecurityService.show_user_menu()

from services.badge_service import (
    BadgeService
)

st.title(
    "👤 Player Profile"
)

players = PlayerService.get_players()

if not players:

    st.warning(
        "No players available."
    )

    st.stop()

player_names = [

    f"{player['firstName']} "
    f"{player['lastName']}"

    for player in players
]

selected_player = st.selectbox(
    "Select Player",
    player_names
)

player = next(

    player

    for player in players

    if (
        f"{player['firstName']} "
        f"{player['lastName']}"
    )
    == selected_player

)

st.subheader(
    "🎯 DUPR Ratings"
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Singles DUPR",
        player.get(
            "currentDuprSingles",
            3.5
        )
    )

with col2:

    st.metric(
        "Doubles DUPR",
        player.get(
            "currentDuprDoubles",
            3.5
        )
    )

col3, col4 = st.columns(2)

with col3:

    st.metric(
        "Previous Singles DUPR",
        player.get(
            "previousDuprSingles",
            3.5
        )
    )

with col4:

    st.metric(
        "Previous Doubles DUPR",
        player.get(
            "previousDuprDoubles",
            3.5
        )
    )

col5, col6 = st.columns(2)

with col5:

    singles_change = round(
        player.get(
            "currentDuprSingles",
            3.5
        )
        -
        player.get(
            "previousDuprSingles",
            3.5
        ),
        3
    )

    st.metric(
        "Singles Change",
        singles_change
    )

with col6:

    doubles_change = round(
        player.get(
            "currentDuprDoubles",
            3.5
        )
        -
        player.get(
            "previousDuprDoubles",
            3.5
        ),
        3
    )

    st.metric(
        "Doubles Change",
        doubles_change
    )



st.divider()

st.subheader(
    "🏓 Singles Statistics"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Singles Wins",
        player.get(
            "singlesWins",
            0
        )
    )

with col2:

    st.metric(
        "Singles Losses",
        player.get(
            "singlesLosses",
            0
        )
    )

with col3:

    st.metric(
        "Singles Win %",
        player.get(
            "singlesWinPercentage",
            0
        )
    )

st.subheader(
    "👥 Doubles Statistics"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Doubles Wins",
        player.get(
            "doublesWins",
            0
        )
    )

with col2:

    st.metric(
        "Doubles Losses",
        player.get(
            "doublesLosses",
            0
        )
    )

with col3:

    st.metric(
        "Doubles Win %",
        player.get(
            "doublesWinPercentage",
            0
        )
    )




st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Matches",
        player["matchesPlayed"]
    )

with col2:

    st.metric(
        "Wins",
        player["wins"]
    )

with col3:

    st.metric(
        "Win %",
        player["winPercentage"]
    )

##Badge services for improvement

st.divider()

st.subheader(
    "🏅 Achievement Badges"
)

badges = (
    BadgeService.get_badges(
        player
    )
)

if badges:

    for badge in badges:

        st.success(
            badge
        )

else:

    st.info(
        "No badges earned yet."
    )

history = [

    record

    for record in RatingService.get_history()

    if record["playerId"]
    == player["id"]

]

singles_history = [

    record

    for record in history

    if record.get(
        "ratingType"
    ) == "Singles"

]

doubles_history = [

    record

    for record in history

    if record.get(
        "ratingType"
    ) == "Doubles"

]

if history:

    st.divider()

    if singles_history:

        st.subheader(
            "📈 Singles DUPR Trend"
        )

        singles_df = pd.DataFrame(
            singles_history
        )

        singles_chart = px.line(

            singles_df,

            x="id",

            y="newRating",

            markers=True,

            title="Singles Rating Progression"

        )

        st.plotly_chart(
            singles_chart,
            use_container_width=True
        )

    if doubles_history:

        st.subheader(
            "📈 Doubles DUPR Trend"
        )

        doubles_df = pd.DataFrame(
            doubles_history
        )

        doubles_chart = px.line(

            doubles_df,

            x="id",

            y="newRating",

            markers=True,

            title="Doubles Rating Progression"

        )

        st.plotly_chart(
            doubles_chart,
            use_container_width=True
        )

    st.subheader(
        "📋 Rating History"
    )

    st.dataframe(
        pd.DataFrame(history),
        use_container_width=True
    )

else:

    st.info(
        "No rating history available."
    )