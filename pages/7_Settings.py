import streamlit as st

from services.security_service import (
    SecurityService
)

SecurityService.require_login()

st.title("⚙️ Settings")

st.subheader("Application Settings")

st.info(
    "Configure application settings here."
)

enable_notifications = st.checkbox(
    "Enable Notifications"
)

default_match_type = st.selectbox(
    "Default Match Type",
    ["Singles", "Doubles"]
)

if st.button("Save Settings"):
    st.success("✅ Settings Saved")