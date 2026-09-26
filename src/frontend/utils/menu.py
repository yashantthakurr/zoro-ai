
from utils.navigation import (
    signin_page,
    signup_page,
    profile_page,
    chat_page,
    logout_page,
    admin_page,
)
import streamlit as st

def authenticated_menu():
    st.sidebar.page_link(profile_page, label="Profile")
    st.sidebar.page_link(chat_page, label="Chat")
    if st.session_state.get("role") == "admin":
        st.sidebar.page_link(admin_page, label="Dashboard")
    st.sidebar.page_link(logout_page, label="Logout")

def unauthenticated_menu():
    st.sidebar.page_link(signin_page, label="Signin")
    st.sidebar.page_link(signup_page, label="Signup")

def menu():
    if st.session_state.get("authenticated", False):
        authenticated_menu()
    else:
        unauthenticated_menu()

def redirect_if_unauthenticated():
    if not st.session_state.get("authenticated", False):
        st.switch_page(signin_page)
        st.stop()

def redirect_if_authenticated():
    if st.session_state.get("authenticated", False):
        st.switch_page(chat_page)
        st.stop()

def redirect_if_not_admin():
    if st.session_state.get("role") != "admin":
        st.switch_page(chat_page)
        st.stop()
