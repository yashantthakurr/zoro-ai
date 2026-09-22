
import streamlit as st

from navigation import (
    signin_page,
    signup_page,
    profile_page,
    chat_page,
    logout_page,
    admin_page
)

if st.session_state.get("authenticated", False):
    if st.session_state.get("role") == "admin":
        pg = st.navigation(
            {
                "Account": [profile_page, logout_page],
                "Activity": [chat_page, admin_page]
            }
        )
    else:
        pg = st.navigation(
            {
                "Account": [profile_page, logout_page],
                "Activity": [chat_page]
            }
        )

else:
    pg = st.navigation([signin_page, signup_page])

pg.run()
