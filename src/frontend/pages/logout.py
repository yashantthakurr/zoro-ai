
from utils.menu import (
    menu,
    redirect_if_unauthenticated
)
from utils.navigation import landing_page
from utils.footer import get_footer
import streamlit as st
import time

st.set_page_config(page_title="Zoro AI | Logout", page_icon="⚔️", layout="centered")

redirect_if_unauthenticated()
menu()

st.title("Zoro AI | Logout")

st.divider()

st.write(f"Are you sure want to logout? Currently logged in as {st.session_state.get('username')}")

if st.button("Logout", type="primary", width="stretch"):
    st.session_state.clear()

    st.success("Logged out successfully. Redirecting to Signin page...")

    time.sleep(1)

    st.switch_page(landing_page)

get_footer()