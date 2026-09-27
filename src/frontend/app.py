
from utils.navigation import (
    admin_page,
    chat_page,
    logout_page,
    profile_page,
    signin_page,
    signup_page,
    landing_page
)
import streamlit as st

pg = st.navigation(
    [landing_page, signin_page, signup_page, profile_page, chat_page, logout_page, admin_page],
    position="hidden",
)

pg.run()
