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

st.title("👥 Player Management")

if st.session_state.get(
    "player_added",
    False
):

    st.success(
        "✅ Player Added Successfully"
    )

    st.balloons()

    del st.session_state[
        "player_added"
    ]

if st.session_state.get(
    "player_updated",
    False
):

    st.success(
        "✅ Player Updated Successfully"
    )

    st.balloons()

    del st.session_state[
        "player_updated"
    ]


if st.session_state.get(
    "player_deleted",
    False
):

    st.success(
        "✅ Player Deleted Successfully"
    )

    st.balloons()

    del st.session_state[
        "player_deleted"
    ]

search_text = st.text_input(
    "🔍 Search Player"
)


players = PlayerService.search_players(
    search_text
)

st.write("Players Found:", len(players))

# Add Player

if role in ["Admin", "Organizer"]:

    with st.expander("➕ Add New Player"):

        with st.form("add_player"):

            first_name = st.text_input(
                "First Name"
            )

            last_name = st.text_input(
                "Last Name"
            )

            email = st.text_input(
                "Email"
            )

            phone = st.text_input(
                "Phone"
            )

            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"]
            )

            age_group = st.selectbox(
                "Age Group",
                [
                    "Under 18",
                    "18-34",
                    "35-49",
                    "50+"
                ]
            )

            add_clicked = st.form_submit_button(
                "Add Player"
            )

            if add_clicked:

                PlayerService.add_player({

                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "phone": phone,
                    "gender": gender,
                    "ageGroup": age_group

                })

                st.session_state[
                    "player_added"
                    ] = True

                st.rerun()


st.subheader(
    "Registered Players"
)

for player in players:

    with st.expander(
        f"{player['firstName']} {player['lastName']}"
    ):


###including doubles and singles

        st.write(
            f"Singles DUPR: "
            f"{player.get('currentDuprSingles', 3.5)}"
        )

        st.write(
            f"Doubles DUPR: "
            f"{player.get('currentDuprDoubles', 3.5)}"
        )


        st.write(
            f"Previous Singles DUPR: "
            f"{player.get('previousDuprSingles', 3.5)}"
        )

        st.write(
            f"Previous Doubles DUPR: "
            f"{player.get('previousDuprDoubles', 3.5)}"
        )



#####including doubles and singles




        st.write(
            f"Matches: {player['matchesPlayed']}"
        )

        st.write(
            f"Wins: {player['wins']}"
        )

        st.write(
            f"Losses: {player['losses']}"
        )

        col1, col2 = st.columns(2)

        #
        # UPDATE PLAYER
        #

        with col1:

            if role in ["Admin", "Organizer"]:

                with st.form(
                    f"edit_{player['id']}"
                ):

                    updated_email = st.text_input(
                        "Email",
                        value=player["email"]
                    )

                    updated_phone = st.text_input(
                        "Phone",
                        value=player["phone"]
                    )

                    update_clicked = (
                        st.form_submit_button(
                            "Update Player"
                        )
                    )

                    if update_clicked:

                        PlayerService.update_player(

                            player["id"],

                            {
                                "email":
                                updated_email,

                                "phone":
                                updated_phone
                            }

                        )

                        st.session_state[
                            "player_updated"
                            ] = True

                        st.rerun()

        #
        # DELETE PLAYER
        #

        with col2:
            if role == "Admin":

                if st.button(
                    f"Delete Player #{player['id']}"
                ):

                    PlayerService.delete_player(
                        player["id"]
                    )

                    st.session_state[
                        "player_deleted"
                        ] = True

                    st.rerun()

if players:

    st.divider()

    st.subheader(
        "Player Grid"
    )

df = pd.DataFrame(players)

df = df.drop(
    columns=[
        "currentDupr",
        "previousDupr"
    ],
    errors="ignore"
)

st.dataframe(
    df,
    use_container_width=True
)