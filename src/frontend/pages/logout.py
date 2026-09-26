
from navigation import signin_page
import streamlit as st
import time

st.set_page_config(page_title="Zoro AI | Logout")

st.title("Zoro AI | Logout")

st.divider()

st.write(f"Are you sure want to logout? Currently logged in as {st.session_state.get('username')}")

if st.button("Logout", type="primary", use_container_width=True):
    st.session_state.clear()

    st.success("Logged out successfully. Redirecting to Signin page...")

    time.sleep(1)

    st.switch_page(signin_page)
