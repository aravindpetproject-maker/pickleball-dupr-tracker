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
role = st.session_state.get("role")

from services.tournament_service import (
    TournamentService
)

from services.round_robin_service import (
    RoundRobinService
)

from services.tournament_standings_service import (
    TournamentStandingsService
)

st.title(
    "🏆 Tournament Manager"
)

if role == "Viewer":

    st.info(
        "👁️ View Only Mode - Tournament management features are disabled."
    )

if "refresh_tournament" in st.session_state:

    del st.session_state[
        "refresh_tournament"
    ]

    st.rerun()

# ===================================
# Create Tournament
# ===================================

players = PlayerService.get_players()

player_names = [

    f"{p['firstName']} "
    f"{p['lastName']}"

    for p in players

]

if role in ["Admin", "Organizer"]:

    with st.form(
        "create_tournament"
    ):

        tournament_name = st.text_input(
            "Tournament Name"
        )

        tournament_type = st.selectbox(
            "Tournament Type",
            [
                "Singles",
                "Doubles"
            ]
        )

        selected_players = st.multiselect(
            "Select Players",
            player_names
        )

        

        create_clicked = st.form_submit_button(
            "Create Tournament"
        )

        if create_clicked:

            if not tournament_name:

                st.error(
                    "Tournament Name is required."
                )

                st.stop()

            

            TournamentService.add_tournament({

                "name":
                tournament_name,

                "type":
                tournament_type,

                "players":
                selected_players,

                "teams":
                [],

                "status":
                "Created",

                "schedule":
                [],

                "champion":
                ""

            })

            st.success(
                "✅ Tournament Created"
            )

            st.rerun()

# ===================================
# Load Tournaments
# ===================================

tournaments = (
    TournamentService.get_tournaments()
)

if not tournaments:

    st.info(
        "No tournaments available."
    )

    st.stop()

st.divider()

# ===================================
# Select Tournament
# ===================================

selected_tournament_name = st.selectbox(

    "Select Tournament",

    [
        tournament["name"]
        for tournament in tournaments
    ]

)

# Always reload latest tournament data

current_tournament = (
    TournamentService
    .get_tournament_by_name(
        selected_tournament_name
    )
)

# ===================================
# Tournament Details
# ===================================

st.subheader(
    "Tournament Details"
)

st.write(
    f"Status: {current_tournament.get('status', 'Created')}"
)

st.write(
    f"Type: {current_tournament.get('type', 'Singles')}"
)

st.write(
    f"Players: {len(current_tournament['players'])}"
)

if current_tournament.get(
    "type"
) == "Doubles":

    teams = current_tournament.get(
        "teams",
        []
    )

    if teams:

        st.subheader(
            "🏓 Teams"
        )

        rows = []

        for team in teams:

            rows.append({

                "Team Name":
                team.get(
                    "teamName",
                    ""
                ),

                "Player 1":
                team.get(
                    "player1",
                    ""
                ),

                "Player 2":
                team.get(
                    "player2",
                    ""
                )

            })

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True
        )

if current_tournament.get(
    "champion"
):

    st.success(
        f"🏆 Champion: {current_tournament['champion']}"
    )



# ===================================
# Team Management
# ===================================

if (
    current_tournament.get(
        "type"
    ) == "Doubles"
    and
    role in ["Admin", "Organizer"]
):

    st.divider()

    st.subheader(
        "🏓 Team Management"
    )

    existing_teams = current_tournament.get(
        "teams",
        []
    )

    if existing_teams:

        st.write(
            "Current Teams"
        )

        team_rows = []

        for team in existing_teams:

            team_rows.append({

                "Team":
                team["teamName"],

                "Player 1":
                team["player1"],

                "Player 2":
                team["player2"]

            })

        st.dataframe(
            pd.DataFrame(
                team_rows
            ),
            use_container_width=True
        )



        team_names = [

            team["teamName"]

            for team in existing_teams

        ]

        team_to_delete = st.selectbox(

            "Select Team To Remove",

            team_names,

            key="delete_team"

        )

        if st.button(
            "🗑 Remove Team"
        ):

            updated_teams = [

                team

                for team in existing_teams

                if team["teamName"]
                != team_to_delete

            ]

            TournamentService.update_tournament(

                current_tournament["id"],

                {
                    "teams": updated_teams
                }

            )

            st.success(
                "✅ Team Removed"
            )

            st.rerun()



    with st.form(
        "add_team"
    ):

        team_name = st.text_input(
            "Team Name"
        )

        player1 = st.selectbox(
            "Player 1",
            current_tournament[
                "players"
            ],
            key="team_player1"
        )

        available_players = [

            p

            for p in current_tournament[
                "players"
            ]

            if p != player1

        ]

        player2 = st.selectbox(
            "Player 2",
            available_players,
            key="team_player2"
        )

        add_team_clicked = (
            st.form_submit_button(
                "➕ Add Team"
            )
        )

        if add_team_clicked:

            if not team_name.strip():

                st.error(
                    "Team Name is required."
                )

                st.stop()

            updated_teams = (
                current_tournament.get(
                    "teams",
                    []
                )
            )


            for team in updated_teams:

                existing_players = [

                    team["player1"],
                    team["player2"]

                ]

                if (
                    player1 in existing_players
                    or
                    player2 in existing_players
                ):

                    st.error(
                        "One or more selected players already belong to a team."
                    )

                    st.stop()

            for team in updated_teams:

                if (
                    team["teamName"].lower()
                    ==
                    team_name.lower()
                ):

                    st.error(
                        "Team name already exists."
                    )

                    st.stop()


            updated_teams.append({

                

                "teamName":
                team_name,

                "player1":
                player1,

                "player2":
                player2

            })

            TournamentService.update_tournament(

                current_tournament[
                    "id"
                ],

                {

                    "teams":
                    updated_teams

                }

            )

            st.success(
                "✅ Team Added"
            )

            st.rerun()



# ===================================
# Generate Schedule
# ===================================

if role in ["Admin", "Organizer"]:

    if st.button(
        "📅 Generate Round Robin Schedule"
    ):

        if (
            current_tournament.get(
                "type",
                "Singles"
            )
            ==
            "Doubles"
        ):

            teams = current_tournament.get(  "teams",  [])

            if len(teams) < 2:

                st.error(
                    "At least 2 teams are required to generate a schedule."
                )

                st.stop()

            schedule = []

            for i in range(
                len(teams)
            ):

                for j in range(
                    i + 1,
                    len(teams)
                ):

                    schedule.append({

                        "team1":
                        teams[i]["teamName"],

                        "team2":
                        teams[j]["teamName"],

                        "team1Player1":
                        teams[i]["player1"],

                        "team1Player2":
                        teams[i]["player2"],

                        "team2Player1":
                        teams[j]["player1"],

                        "team2Player2":
                        teams[j]["player2"]

                    })

        else:

            schedule = (
                RoundRobinService
                .generate_schedule(
                    current_tournament[
                        "players"
                    ]
                )
            )

        TournamentService.update_tournament(

            current_tournament[
                "id"
            ],

            {

                "schedule":
                schedule,

                "status":
                "Scheduled"

            }

        )

        st.success(
            "✅ Schedule Generated"
        )

        st.rerun()

# ===================================
# Schedule
# ===================================

schedule = current_tournament.get(
    "schedule",
    []
)

if schedule:

    st.divider()

    st.subheader(
        "📅 Tournament Schedule"
    )

    completed_matches = len(
        [
            match
            for match in schedule
            if match.get("winner")
        ]
    )

    total_matches = len(
        schedule
    )

    if total_matches > 0:

        st.subheader(
            "📊 Tournament Progress"
        )

        st.progress(
            completed_matches /
            total_matches
        )

        st.write(
            f"{completed_matches} of "
            f"{total_matches} matches completed"
        )

    tournament_type = current_tournament.get(
        "type",
        "Singles"
    )

    # ==========================
    # Singles Tournament
    # ==========================

    if tournament_type == "Singles":

        display_rows = []

        for match in schedule:

            display_rows.append({

                "Player 1":
                match.get(
                    "player1",
                    ""
                ),

                "Player 2":
                match.get(
                    "player2",
                    ""
                ),

                "Score":
                (
                    f"{match.get('scorePlayer1','')} - "
                    f"{match.get('scorePlayer2','')}"
                ),

                "Winner":
                match.get(
                    "winner",
                    ""
                )

            })

        st.dataframe(
            pd.DataFrame(
                display_rows
            ),
            use_container_width=True
        )

    # ==========================
    # Doubles Tournament
    # ==========================

    else:

        display_rows = []

        for match in schedule:

            display_rows.append({

                "Team 1":
                match.get(
                    "team1",
                    ""
                ),

                "Team 1 Players":
                (
                    f"{match.get('team1Player1','')} / "
                    f"{match.get('team1Player2','')}"
                ),

                "Team 2":
                match.get(
                    "team2",
                    ""
                ),

                "Team 2 Players":
                (
                    f"{match.get('team2Player1','')} / "
                    f"{match.get('team2Player2','')}"
                ),

                "Score":
                (
                    f"{match.get('scoreTeam1','')} - "
                    f"{match.get('scoreTeam2','')}"
                ),

                "Winner":
                match.get(
                    "winner",
                    ""
                )

            })

        st.dataframe(
            pd.DataFrame(
                display_rows
            ),
            use_container_width=True
        )

    
# ===================================
# Standings
# ===================================

if schedule:

    standings = (

        TournamentStandingsService
        .calculate_standings(
            current_tournament
        )

    )

    if standings:

        st.divider()

        st.subheader(
            "🏆 Tournament Standings"
        )

        standings_df = pd.DataFrame(
            standings
        )

        st.dataframe(
            standings_df,
            use_container_width=True
        )

        leader = standings[0]

        st.success(

            f"🏆 Current Leader: "
            f"{leader['Player']} "
            f"({leader['Points']} points)"

        )

        completed_matches = len(

            [
                match
                for match in schedule
                if match.get("winner")
            ]

        )

        total_matches = len(
            schedule
        )


        st.write(
            "Completed Matches:",
            completed_matches
        )

        st.write(
            "Total Matches:",
            total_matches
        )

        if (
            total_matches > 0
            and
            completed_matches == total_matches
        ):



            champion = (
                standings[0]["Player"]
            )

            if (
                current_tournament.get(
                    "champion"
                )
                != champion
            ):

                TournamentService.update_tournament(

                    current_tournament["id"],

                    {

                        "status":
                        "Completed",

                        "champion":
                        champion

                    }

                )
            st.rerun()

            st.balloons()

            st.success(
                f"🏆 Tournament Champion: {champion}"
            )


# ===================================
# Tournament Actions
# ===================================

if role in ["Admin", "Organizer"]:

    st.divider()

    st.subheader(
        "⚙️ Tournament Actions"
    )

    col1, col2 = st.columns(2)

    # ---------------------------
    # EDIT TOURNAMENT
    # ---------------------------

    with col1:

        with st.form(
            f"edit_tournament_{current_tournament['id']}"
        ):

            updated_name = st.text_input(
                "Tournament Name",
                value=current_tournament["name"]
            )

            updated_status = st.selectbox(
                "Tournament Status",
                [
                    "Created",
                    "Scheduled",
                    "Completed"
                ],
                index=[
                    "Created",
                    "Scheduled",
                    "Completed"
                ].index(
                    current_tournament.get(
                        "status",
                        "Created"
                    )
                )
            )

            update_clicked = st.form_submit_button(
                "💾 Update Tournament"
            )

            if update_clicked:

                TournamentService.update_tournament(
                    current_tournament["id"],
                    {
                        "name": updated_name,
                        "status": updated_status
                    }
                )

                st.success(
                    "✅ Tournament Updated"
                )

                st.rerun()

    # ---------------------------
    # DELETE TOURNAMENT
    # ---------------------------

    with col2:

        if role == "Admin":

            if st.button(
                "🗑 Delete Tournament"
            ):

                TournamentService.delete_tournament(
                    current_tournament["id"]
                )

                st.success(
                    "Tournament Deleted"
                )

                st.rerun()

else:

    st.divider()

    st.info(
        "👁️ View Only Mode - Tournament modifications are disabled."
    )