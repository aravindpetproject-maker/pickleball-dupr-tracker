import streamlit as st
import pandas as pd

from services.player_service import (
    PlayerService
)

from services.match_service import (
    MatchService
)

from services.dashboard_stats_service import (
    DashboardStatsService
)


from services.security_service import (
    SecurityService
)

SecurityService.show_user_menu()
SecurityService.require_login()


if (
    "dashboard_visit_logged"
    not in st.session_state
):

    DashboardStatsService.increment_views()

    st.session_state[
        "dashboard_visit_logged"
    ] = True



from services.tournament_service import (
    TournamentService
)

from services.analytics_service import (
    AnalyticsService
)

st.title("🏓 Pickleball DUPR Tracker")

players = PlayerService.get_players()

matches = MatchService.get_matches()

# =====================================================
# KPI CARDS
# =====================================================

total_players = len(players)

total_matches = len(matches)

singles_matches = len([
    match
    for match in matches
    if match.get("matchType") == "Singles"
])

doubles_matches = len([
    match
    for match in matches
    if match.get("matchType") == "Doubles"
])

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "👥 Players",
        total_players
    )

with col2:

    st.metric(
        "🏓 Matches",
        total_matches
    )

with col3:

    st.metric(
        "🎯 Singles",
        singles_matches
    )

with col4:

    st.metric(
        "👥 Doubles",
        doubles_matches
    )


# =====================================================
# TOURNAMENT SUMMARY
# =====================================================

st.divider()

st.subheader(
    "🏆 Tournament Summary"
)

tournaments = (
    TournamentService.get_tournaments()
)

active_tournaments = [
    t
    for t in tournaments
    if t.get(
        "status",
        "Active"
    ) != "Completed"
]

completed_tournaments = [
    t
    for t in tournaments
    if t.get(
        "status"
    ) == "Completed"
]

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Active Tournaments",
        len(active_tournaments)
    )

with col2:

    st.metric(
        "Completed Tournaments",
        len(completed_tournaments)
    )

with col3:

    st.metric(
        "Total Tournaments",
        len(tournaments)
    )



# =====================================================
# ACTIVE TOURNAMENT LEADERBOARD
# =====================================================

st.divider()

st.subheader(
    "🥇 Active Tournament Leaderboard"
)

if active_tournaments:

    selected_tournament = st.selectbox(
        "Select Tournament",
        [
            t["name"]
            for t in active_tournaments
        ]
    )

    tournament = next(
        (
            t
            for t in active_tournaments
            if t["name"]
            == selected_tournament
        ),
        None
    )

    standings = []

    if tournament:

        standings = tournament.get(
            "standings",
            []
        )

    if standings:

        standings_df = pd.DataFrame(
            standings
        )

        st.dataframe(
            standings_df,
            use_container_width=True
        )

    else:

        st.info(
            "No leaderboard data available yet."
        )

else:

    st.info(
        "No active tournaments available."
    )


# =====================================================
# LEAGUE LEADERS
# =====================================================

if players:

    st.divider()

    st.subheader(
        "🏆 League Leaders"
    )

    singles_leader = max(
        players,
        key=lambda p:
        p.get(
            "currentDuprSingles",
            3.5
        )
    )

    doubles_leader = max(
        players,
        key=lambda p:
        p.get(
            "currentDuprDoubles",
            3.5
        )
    )

    best_win_pct = max(
        players,
        key=lambda p:
        p.get(
            "winPercentage",
            0
        )
    )

    most_active = max(
        players,
        key=lambda p:
        p.get(
            "matchesPlayed",
            0
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🏓 Singles Leader",
            f"{singles_leader['firstName']} "
            f"{singles_leader['lastName']}",
            round(
                singles_leader.get(
                    "currentDuprSingles",
                    3.5
                ),
                3
            )
        )

    with col2:

        st.metric(
            "👥 Doubles Leader",
            f"{doubles_leader['firstName']} "
            f"{doubles_leader['lastName']}",
            round(
                doubles_leader.get(
                    "currentDuprDoubles",
                    3.5
                ),
                3
            )
        )

    with col3:

        st.metric(
            "🎯 Best Win %",
            f"{best_win_pct['firstName']} "
            f"{best_win_pct['lastName']}",
            f"{best_win_pct.get('winPercentage',0)}%"
        )

    with col4:

        st.metric(
            "🔥 Most Active",
            f"{most_active['firstName']} "
            f"{most_active['lastName']}",
            f"{most_active.get('matchesPlayed',0)} Matches"
        )

# =====================================================
# RECENT ACTIVITY
# =====================================================

st.divider()

st.subheader(
    "📢 Recent Activity"
)

recent_matches = sorted(
    matches,
    key=lambda x:
    x.get("id", 0),
    reverse=True
)[:5]

if recent_matches:

    for match in recent_matches:

        st.info(
            f"✅ {match.get('winner')} won a "
            f"{match.get('matchType')} match "
            f"({match.get('scoreA')} - "
            f"{match.get('scoreB')})"
        )

else:

    st.info(
        "No recent matches available."
    )

# =====================================================
# TOP 5 SINGLES PLAYERS
# =====================================================

st.divider()

st.subheader(
    "🥇 Top 5 Singles Rankings"
)

top_singles = sorted(
    players,
    key=lambda p:
    p.get(
        "currentDuprSingles",
        3.5
    ),
    reverse=True
)[:5]

top_singles_df = pd.DataFrame([

    {
        "Rank":
        idx + 1,

        "Player":
        f"{player['firstName']} "
        f"{player['lastName']}",

        "Singles DUPR":
        round(
            player.get(
                "currentDuprSingles",
                3.5
            ),
            3
        ),

        "Win %":
        player.get(
            "winPercentage",
            0
        )
    }

    for idx, player
    in enumerate(top_singles)

])

st.dataframe(
    top_singles_df,
    use_container_width=True
)

# =====================================================
# TOP 5 DOUBLES PLAYERS
# =====================================================

st.divider()

st.subheader(
    "👥 Top 5 Doubles Rankings"
)

top_doubles = sorted(
    players,
    key=lambda p:
    p.get(
        "currentDuprDoubles",
        3.5
    ),
    reverse=True
)[:5]

top_doubles_df = pd.DataFrame([

    {
        "Rank":
        idx + 1,

        "Player":
        f"{player['firstName']} "
        f"{player['lastName']}",

        "Doubles DUPR":
        round(
            player.get(
                "currentDuprDoubles",
                3.5
            ),
            3
        ),

        "Win %":
        player.get(
            "winPercentage",
            0
        )
    }

    for idx, player
    in enumerate(top_doubles)

])

st.dataframe(
    top_doubles_df,
    use_container_width=True
)

# =====================================================
# MOST IMPROVED PLAYERS
# =====================================================

st.divider()

st.subheader(
    "🔥 Most Improved Players"
)

improved_players = (
    AnalyticsService
    .get_most_improved_players()
)

if improved_players:

    st.dataframe(
        pd.DataFrame(
            improved_players[:5]
        ),
        use_container_width=True
    )

else:

    st.info(
        "No improvement data available."
    )

# =====================================================
# QUICK SUMMARY
# =====================================================

st.divider()

st.subheader(
    "📈 League Summary"
)

st.success(
    f"League currently has "
    f"{total_players} players and "
    f"{total_matches} matches recorded."
)

st.info(
    f"{singles_matches} Singles matches "
    f"and {doubles_matches} Doubles matches "
    f"have been played."
)

