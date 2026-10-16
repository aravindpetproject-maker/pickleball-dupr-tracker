import streamlit as st
import pandas as pd
import plotly.express as px

from services.analytics_service import (
    AnalyticsService
)

from services.security_service import (
    SecurityService
)

SecurityService.require_login()

SecurityService.show_user_menu()

st.title(
    "🚀 Most Improved Players"
)

players = (
    AnalyticsService
    .get_most_improved_players()
)

if players:

    st.subheader(
        "Player Improvement Rankings"
    )

    df = pd.DataFrame(
        players
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    top_player = df.iloc[0]

    st.success(

        f"🏆 Most Improved Player: "
        f"{top_player['Player']} "
        f"({top_player['Improvement']:+.3f})"

    )

else:

    st.info(
        "No rating history available."
    )

fig = px.bar(

    df,

    x="Player",

    y="Improvement",

    title="Player Improvement Rankings"

)

st.plotly_chart(
    fig,
    use_container_width=True
)