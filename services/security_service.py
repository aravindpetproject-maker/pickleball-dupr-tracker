import streamlit as st


class SecurityService:

    @staticmethod
    def is_logged_in():

        return st.session_state.get(
            "logged_in",
            False
        )

    @staticmethod
    def require_login():

        if not SecurityService.is_logged_in():

            if "role" not in st.session_state:
                st.session_state["role"] = "Viewer"

            if "username" not in st.session_state:
                st.session_state["username"] = "Anonymous"

        return

    @staticmethod
    def is_admin():

        return (
            st.session_state.get(
                "role"
            )
            == "Admin"
        )

    @staticmethod
    def is_organizer():

        return (
            st.session_state.get(
                "role"
            )
            in [
                "Admin",
                "Organizer"
            ]
        )

    @staticmethod
    def require_admin():

        SecurityService.require_login()

        if not SecurityService.is_admin():

            st.error(
                "Admin access required."
            )

            st.stop()

    @staticmethod
    def require_organizer():

        SecurityService.require_login()

        if not SecurityService.is_organizer():

            st.error(
                "Access denied."
            )

            st.stop()

    @staticmethod
    def show_user_menu():

        username = st.session_state.get(
            "username",
            "Anonymous"
        )

        role = st.session_state.get(
            "role",
            "Viewer"
        )

        st.sidebar.success(
            f"👤 {username}"
        )

        st.sidebar.info(
            f"Role: {role}"
        )

        if role != "Viewer":

            if st.sidebar.button(
                "🚪 Logout"
            ):

                st.session_state.clear()

                st.session_state["role"] = "Viewer"
                st.session_state["username"] = "Anonymous"

                st.rerun()