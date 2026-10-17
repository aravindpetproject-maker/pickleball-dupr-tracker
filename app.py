import streamlit as st

from services.auth_service import (
    AuthService
)

# ===================================
# Redirect Logged In Users
# ===================================

if st.session_state.get(
    "logged_in",
    False
):

    st.switch_page(
        "pages/1_Dashboard.py"
    )

# ===================================
# Page Header
# ===================================

st.title(
    "🏓 Montebello Pickleball DUPR Tracker"
)

st.subheader(
    "🔐 Login"
)

# ===================================
# Login Form
# ===================================

username = st.text_input(
    "Username"
)

password = st.text_input(
    "Password",
    type="password"
)

col1, col2 = st.columns(2)

# ===================================
# Login Button
# ===================================

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

            st.switch_page(
                "pages/1_Dashboard.py"
            )

        else:

            st.error(
                "Invalid username or password"
            )

# ===================================
# Continue As Viewer
# ===================================

with col2:

    if st.button(
        "👁 Continue as Viewer",
        use_container_width=True
    ):

        st.session_state[
            "logged_in"
        ] = True

        st.session_state[
            "username"
        ] = "Guest"

        st.session_state[
            "role"
        ] = "Viewer"

        st.switch_page(
            "pages/1_Dashboard.py"
        )

# ===================================
# Footer
# ===================================

st.divider()

st.caption(
    "Viewer mode provides read-only access to dashboards, rankings, tournaments, and reports."
)