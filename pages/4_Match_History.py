import streamlit as st
import pandas as pd

from services.match_service import (
    MatchService
)

from services.tournament_service import (
    TournamentService
)

from services.security_service import (
    SecurityService
)

SecurityService.require_login()
SecurityService.show_user_menu()
role = st.session_state.get("role")

st.title("📋 Match History")

# =====================================
# Success Messages
# =====================================

if st.session_state.get(
    "match_updated",
    False
):

    st.success(
        "✅ Match Updated Successfully"
    )

    st.info(
        "👉 Go to Analytics and click "
        "'Recalculate All Ratings' "
        "to rebuild DUPR ratings."
    )

    st.balloons()

    del st.session_state[
        "match_updated"
    ]

if st.session_state.get(
    "match_deleted",
    False
):

    st.success(
        "✅ Match Deleted Successfully"
    )

    st.balloons()

    del st.session_state[
        "match_deleted"
    ]

# =====================================
# Load Matches
# =====================================

matches = MatchService.get_matches()

if not matches:

    st.info(
        "No matches found."
    )

    st.stop()

# =====================================
# Match Grid
# =====================================

st.subheader(
    "Match History"
)

st.dataframe(
    pd.DataFrame(matches),
    use_container_width=True
)

st.divider()

# =====================================
# Edit Match
# =====================================

st.subheader(
    "📄 Match Details"
)

if role == "Viewer":

    st.info(
        "👁️ View Only Mode"
    )

match_ids = [
    match["id"]
    for match in matches
]

selected_match_id = st.selectbox(
    "Select Match",
    match_ids
)

selected_match = next(
    match
    for match in matches
    if match["id"] == selected_match_id
)

match_type = selected_match.get(
    "matchType",
    "Singles"
)

st.write(
    f"Match Type: {match_type}"
)

# =====================================
# Singles Match Details
# =====================================

if match_type == "Singles":

    st.write(
        f"Player A: "
        f"{selected_match.get('playerA', '')}"
    )

    st.write(
        f"Player B: "
        f"{selected_match.get('playerB', '')}"
    )

# =====================================
# Doubles Match Details
# =====================================

else:

    st.write(
        f"Team A Player 1: "
        f"{selected_match.get('teamAPlayer1', '')}"
    )

    st.write(
        f"Team A Player 2: "
        f"{selected_match.get('teamAPlayer2', '')}"
    )

    st.write(
        f"Team B Player 1: "
        f"{selected_match.get('teamBPlayer1', '')}"
    )

    st.write(
        f"Team B Player 2: "
        f"{selected_match.get('teamBPlayer2', '')}"
    )

score_a = st.number_input(
    "Score A",
    min_value=0,
    max_value=30,
    value=int(
        selected_match.get(
            "scoreA",
            0
        )
    ),
    key="score_a"
)

score_b = st.number_input(
    "Score B",
    min_value=0,
    max_value=30,
    value=int(
        selected_match.get(
            "scoreB",
            0
        )
    ),
    key="score_b"
)

notes = st.text_area(
    "Notes",
    value=selected_match.get(
        "notes",
        ""
    )
)

# =====================================
# Update Match
# =====================================

if role in ["Admin", "Organizer"]:

    if st.button(
        "💾 Update Match"
    ):

        if match_type == "Singles":

            if score_a > score_b:

                winner = selected_match.get(
                    "playerA",
                    ""
                )

            else:

                winner = selected_match.get(
                    "playerB",
                    ""
                )

        else:

            if score_a > score_b:

                winner = selected_match.get(
                    "teamNameA",
                    "Team A"
                )

            else:

                winner = selected_match.get(
                    "teamNameB",
                    "Team B"
                )

    MatchService.update_match(

        selected_match_id,

        {

            "scoreA": score_a,

            "scoreB": score_b,

            "winner": winner,

            "notes": notes

        }

    )

    # =====================================
    # Update Tournament Schedule
    # =====================================

    if selected_match.get(
        "isTournamentMatch"
    ):

        if match_type == "Singles":

            TournamentService.record_match_result(

                selected_match.get(
                    "tournamentName"
                ),

                selected_match.get(
                    "playerA"
                ),

                selected_match.get(
                    "playerB"
                ),

                winner,

                score_a,

                score_b

            )

        else:

            team1_name = selected_match.get(
                "teamNameA"
            )

            team2_name = selected_match.get(
                "teamNameB"
            )


######debug

            st.write(
                "Tournament:",
                selected_match.get(
                "tournamentName"
                )
            )

            st.write(
                "Team1:",
                selected_match.get(
                "teamNameA"
                )
            )

            st.write(
                "Team2:",
                selected_match.get(
                "teamNameB"
                )
            )

            st.write(
                "Winner:",
                winner
            )

            st.write(
                "Scores:",
                score_a,
                score_b
            )




######debug





            if team1_name and team2_name:

                TournamentService.record_doubles_match_result(

                    selected_match.get(
                        "tournamentName"
                    ),

                    team1_name,

                    team2_name,

                    winner,

                    score_a,

                    score_b

                )

    st.session_state[
        "match_updated"
    ] = True

    st.session_state[
        "refresh_tournament"
    ] = True

    st.rerun()