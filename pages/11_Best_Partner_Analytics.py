import streamlit as st
import pandas as pd

from services.partner_analytics_service import (
    PartnerAnalyticsService
)

from services.security_service import (
    SecurityService
)

SecurityService.require_login()

SecurityService.show_user_menu()

st.title(
    "👥 Best Partner Analytics"
)

partner_stats = (
    PartnerAnalyticsService
    .get_partner_stats()
)

rows = []

for team, stats in (
    partner_stats.items()
):

    matches = stats["matches"]

    wins = stats["wins"]

    win_pct = round(
        (
            wins / matches
        ) * 100,
        2
    )

    rows.append({

        "Player 1":
        team[0],

        "Player 2":
        team[1],

        "Matches":
        matches,

        "Wins":
        wins,

        "Win %":
        win_pct

    })

if rows:

    df = pd.DataFrame(rows)

    df = df.sort_values(
        by="Win %",
        ascending=False
    )

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "No doubles matches available."
    )