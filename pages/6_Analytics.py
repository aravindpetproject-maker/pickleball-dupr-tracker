import streamlit as st
import pandas as pd
import io
import os

from services.analytics_service import (
    AnalyticsService
)

from services.security_service import (
    SecurityService
)

SecurityService.require_login()

SecurityService.show_user_menu()
role = st.session_state.get("role")

from services.recalculation_service import (
    RecalculationService
)

from services.backup_service import (
    BackupService
)

st.title(
    "📊 Analytics"
)

# ============================
# Display Success Message
# ============================

if "recalc_result" in st.session_state:

    result = st.session_state[
        "recalc_result"
    ]

    st.success(
        f"✅ Rating Recalculation Completed Successfully!\n\n"
        f"Players Updated: {result['players']}\n"
        f"Matches Processed: {result['matches']}\n"
        f"Rating Records Rebuilt: {result['ratings']}"
    )

    st.balloons()

    del st.session_state[
        "recalc_result"
    ]

# ============================
# System Maintenance
# ============================

if role == "Admin":

    st.divider()

    st.subheader(
        "System Maintenance"
    )

    st.info(
        "Use this option after correcting match scores."
    )

    if st.button(
        "🔄 Recalculate All Ratings"
    ):

        result = (
            RecalculationService
            .recalculate_all()
        )

        st.session_state[
            "recalc_result"
        ] = result

        st.rerun()


# ============================
# Backup Management
# ============================

st.divider()

st.subheader(
    "💾 Backup Management"
)

st.info(
    "Create a backup of all application data."
)

if st.button(
    "💾 Backup Data"
):

    backup_folder = (
        BackupService.create_backup()
    )

    st.success(
        "✅ Backup Created Successfully"
    )

    st.write(
        f"Location: {backup_folder}"
    )


# ============================
# Existing Backups
# ============================

import os

st.subheader(
    "📁 Available Backups"
)

if os.path.exists("backups"):

    backup_list = sorted(
        os.listdir("backups"),
        reverse=True
    )

    if backup_list:

        for backup in backup_list:

            st.write(
                f"📁 {backup}"
            )

    else:

        st.info(
            "No backups found."
        )

else:

    st.info(
        "Backups folder does not exist."
    )

# ============================
# Restore Backups
# ============================

if role == "Admin":
    st.divider()

    st.subheader(
        "♻️ Restore Backup"
    )

    backups = (
        BackupService
        .get_backups()
    )

    if backups:

        selected_backup = (
            st.selectbox(
                "Select Backup",
                backups
            )
        )

        if st.button(
            "♻️ Restore Selected Backup"
        ):

            success = (
                BackupService
                .restore_backup(
                    selected_backup
                )
            )

            if success:

                st.success(
                    f"✅ Restored {selected_backup}"
                )

                st.warning(
                    "Restart Streamlit "
                    "to reload data."
                )

            else:

                st.error(
                    "Restore failed."
                )

# ============================
# Leaderboard
# ============================

st.divider()

st.subheader(
    "🏆 Leaderboard"
)

leaderboard = (
    AnalyticsService
    .get_leaderboard()
)

if leaderboard:

    leaderboard_df = pd.DataFrame([
    {
        "Player":
        f"{player['firstName']} "
        f"{player['lastName']}",

        "Singles DUPR":
        player.get(
            "currentDuprSingles",
            3.5
        ),

        "Doubles DUPR":
        player.get(
            "currentDuprDoubles",
            3.5
        ),

        "Wins":
        player["wins"],

        "Losses":
        player["losses"],

        "Win %":
        player["winPercentage"]

    }

    for player in leaderboard

])

    st.dataframe(
        leaderboard_df,
        use_container_width=True
    )

    excel_buffer = io.BytesIO()

    leaderboard_df.to_excel(
        excel_buffer,
        index=False
    )

    st.download_button(

        label="📥 Download Leaderboard Excel",

        data=excel_buffer.getvalue(),

        file_name="leaderboard.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

else:

    st.info(
        "No players available."
    )

# ============================
# Top Win Percentage
# ============================

st.divider()

st.subheader(
    "🔥 Top Win Percentage"
)

top_winners = (
    AnalyticsService
    .get_top_win_percentage()
)

if top_winners:

    winners_df = pd.DataFrame([
        {
            "Player":
            f"{player['firstName']} "
            f"{player['lastName']}",

            "Win %":
            player["winPercentage"],

            "Matches":
            player["matchesPlayed"],

            "Wins":
            player["wins"],

            "Losses":
            player["losses"]
        }
        for player in top_winners
    ])

    st.dataframe(
        winners_df,
        use_container_width=True
    )

# ============================
# Summary
# ============================

st.divider()

st.subheader(
    "📈 Summary"
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Players",
        len(leaderboard)
    )

with col2:

    st.metric(
        "Total Matches",
        sum(
            p["matchesPlayed"]
            for p in leaderboard
        ) // 2
        if leaderboard
        else 0
    )

# ============================
# Doubles match
# ============================

match_counts = (
    AnalyticsService
    .get_match_type_counts()
)

st.divider()

st.subheader(
    "🏓 Match Types"
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Singles",
        match_counts["singles"]
    )

with col2:

    st.metric(
        "Doubles",
        match_counts["doubles"]
    )