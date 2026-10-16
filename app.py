import streamlit as st

from services.auth_service import (
    AuthService
)

# If already logged in, go to Dashboard
if st.session_state.get(
    "logged_in",
    False
):

    st.switch_page(
        "pages/1_Dashboard.py"
    )

st.title(
    "🏓 Montebello Pickleball DUPR Tracker"
)

st.subheader(
    "🔐 Login"
)

username = st.text_input(
    "Username"
)

password = st.text_input(
    "Password",
    type="password"
)

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "Login",
        use_container_width=True
    ):

        user = AuthService.login(
            username,
            password
        )

        if user:

            st.session_state[
                "logged_in"
            ] = True

            st.session_state[
                "username"
            ] = user[
                "username"
            ]

            st.session_state[
                "role"
            ] = user[
                "role"
            ]

            st.rerun()

        else:

            st.error(
                "Invalid username or password"
            )

with col2:

    if st.button(
        "👁 Continue as Viewer",
        use_container_width=True
    ):

        st.session_state[
            "logged_in"
        ] = False

     