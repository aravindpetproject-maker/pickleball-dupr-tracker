import streamlit as st
import pandas as pd
import plotly.express as px

from services.player_service import (
    PlayerService
)

from services.security_service import (
    SecurityService
)

SecurityService.require_login()

SecurityService.show_user_menu()

from services.analytics_service import (
    AnalyticsService
)

from services.badge_service import (
    BadgeService
)

st.title(
    "🏆 Player Rankings"
)

players = PlayerService.get_players()

if not players:

    st.info(
        "No players available."
    )

    st.stop()

improvement_data = (
    AnalyticsService
    .get_most_improved_players()
)

improvement_map = {

    item["Player"]:
    item["Improvement"]

    for item in improvement_data

}

rankings = []

ranking_type = st.selectbox(
    "Ranking Type",
    [
        "Singles DUPR",
        "Doubles DUPR",
        "Win Percentage",
        "Most Wins",
        "Most Matches Played"
    ]
)

if ranking_type == "Singles DUPR":

    sorted_players = sorted(
        players,
        key=lambda p:
        p.get(
            "currentDuprSingles",
            3.5
        ),
        reverse=True
    )

elif ranking_type == "Doubles DUPR":

    sorted_players = sorted(
        players,
        key=lambda p:
        p.get(
            "currentDuprDoubles",
            3.5
        ),
        reverse=True
    )

elif ranking_type == "Win Percentage":

    sorted_players = sorted(
        players,
        key=lambda p:
        p.get(
            "winPercentage",
            0
        ),
        reverse=True
    )

elif ranking_type == "Most Wins":

    sorted_players = sorted(
        players,
        key=lambda p:
        p.get(
            "wins",
            0
        ),
        reverse=True
    )

else:

    sorted_players = sorted(
        players,
        key=lambda p:
        p.get(
            "matchesPlayed",
            0
        ),
        reverse=True
    )

for rank, player in enumerate(
    sorted_players,
    start=1
):

    player_name = (
        f"{player['firstName']} "
        f"{player['lastName']}"
    )

    badges = (
        BadgeService.get_badges(
            player
        )
    )

    rankings.append({

        "Rank":
        rank,

        "Player":
        player_name,

        "Singles DUPR":
        round(
            player.get(
                "currentDuprSingles",
                3.5
            ),
            3
        ),

        "Doubles DUPR":
        round(
            player.get(
                "currentDuprDoubles",
                3.5
            ),
            3
        ),

        "Singles W-L":
        f"{player.get('singlesWins',0)}-"
        f"{player.get('singlesLosses',0)}",

        "Doubles W-L":
        f"{player.get('doublesWins',0)}-"
        f"{player.get('doublesLosses',0)}",

        "Singles Win %":
        player.get(
            "singlesWinPercentage",
            0
        ),

        "Doubles Win %":
        player.get(
            "doublesWinPercentage",
            0
        ),


        "Overall Win %":
        player.get(
            "winPercentage",
            0
        ),

        "Matches":
        player.get(
            "matchesPlayed",
            0
        ),

        "Improvement":
        improvement_map.get(
            player_name,
            0
        ),

        "Badges":
        len(badges)
    })

ranking_df = pd.DataFrame(
    rankings
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

st.divider()

st.subheader(
    "🥇 Top 3 Players"
)

top_three = ranking_df.head(3)

for _, row in top_three.iterrows():

    st.success(

        f"#{row['Rank']} "
        f"{row['Player']} | "
        f"Singles: {row['Singles DUPR']} | "
        f"Doubles: {row['Doubles DUPR']}"


    )

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    top_rated = ranking_df.iloc[0]

    st.metric(
        "Top Rated Player",
        top_rated["Player"]
    )

with col2:

    best_win_pct = max(
        players,
        key=lambda p:
        p["winPercentage"]
    )

    st.metric(
        "Best Win %",
        f"{best_win_pct['winPercentage']}%"
    )

with col3:

    most_active = max(
        players,
        key=lambda p:
        p["matchesPlayed"]
    )

    st.metric(
        "Most Active",
        f"{most_active['firstName']} "
        f"{most_active['lastName']}",
        f"{most_active['matchesPlayed']} Matches"
    )



metric_column = (
    "Singles DUPR"
    if ranking_type == "Singles DUPR"
    else
    "Doubles DUPR"
    if ranking_type == "Doubles DUPR"
    else
    "Overall Win %"
)

fig = px.bar(

    ranking_df,

    x="Player",

    y=metric_column,

    color=metric_column,

    title=f"{ranking_type} Rankings"
)







st.plotly_chart(
    fig,
    use_container_width=True
)



st.divider()

st.subheader(
    "⭐ Hall Of Fame"
)

col1, col2 = st.columns(2)

with col1:

    highest_singles = max(
        players,
        key=lambda p:
        p.get(
            "currentDuprSingles",
            3.5
        )
    )

    st.metric(
        "Highest Singles DUPR",
        highest_singles[
            "currentDuprSingles"
        ],
        f"{highest_singles['firstName']} "
        f"{highest_singles['lastName']}"
    )

with col2:

    highest_doubles = max(
        players,
        key=lambda p:
        p.get(
            "currentDuprDoubles",
            3.5
        )
    )

    st.metric(
        "Highest Doubles DUPR",
        highest_doubles[
            "currentDuprDoubles"
        ],
        f"{highest_doubles['firstName']} "
        f"{highest_doubles['lastName']}"
    )


col1, col2 = st.columns(2)

with col1:

    singles_leader = max(
        players,
        key=lambda p:
        p.get(
            "currentDuprSingles",
            3.5
        )
    )

    st.info(
        f"🏓 Singles Leader: "
        f"{singles_leader['firstName']} "
        f"{singles_leader['lastName']}"
    )

with col2:

    doubles_leader = max(
        players,
        key=lambda p:
        p.get(
            "currentDuprDoubles",
            3.5
        )
    )

    st.info(
        f"👥 Doubles Leader: "
        f"{doubles_leader['firstName']} "
        f"{doubles_leader['lastName']}"
    )