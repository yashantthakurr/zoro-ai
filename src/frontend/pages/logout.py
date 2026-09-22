
import streamlit as st
import requests
import time
from navigation import signin_page

st.set_page_config(page_title="Zoro AI | Logout")

st.title("Zoro AI | Logout")

st.divider()

st.write(f"Are you sure want to logout? Currently logged in as {st.session_state.get("username")}")

if st.button("Logout", type="primary", use_container_width=True):

    st.session_state["access_token"] = None
    st.session_state["authenticated"] = False

    st.success("Logged out successfully. Redirecting to Signup page...")

    time.sleep(1.5)

    st.switch_page(signin_page)
