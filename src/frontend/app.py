
from pathlib import Path
from utils.navigation import (
    signin_page,
    signup_page,
    profile_page,
    chat_page,
    logout_page,
    admin_page
)
import streamlit as st
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

pg = st.navigation(
    [signin_page, signup_page, profile_page, chat_page, logout_page, admin_page],
    position="hidden",
)

pg.run()
