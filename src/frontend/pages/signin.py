
from src.backend.constants.config import secrets
from utils.menu import redirect_if_authenticated
from utils.navigation import signup_page, chat_page
import requests
import streamlit as st
import time

st.set_page_config(page_title="Zoro AI | Signin", page_icon="⚔️")

redirect_if_authenticated()

st.title("Zoro AI | Signin to your account")

st.divider()

SIGNIN_URL = f"{secrets.BACKEND_BASE_URL}/auth/signin"

username = st.text_input(label="Username", max_chars=24)
password = st.text_input(label="Password", type="password", max_chars=64)

if st.button("Signin", use_container_width=True, type="primary"):
    if not username or not password:
        st.warning("All fields are required.")
    elif len(username) < 4:
        st.warning("Username must be of 4 characters.")
    elif len(password) < 8:
        st.warning("Password must be of 8 characters.")
    else:
        try:
            with st.spinner("Signing you in. Please wait..."):
                response = requests.post(url=SIGNIN_URL, json={"username": username, "password": password}, timeout=10)
                if response.status_code==200:
                    st.success("Signed in successfully! Redirecting to chat page...")
                    st.session_state["access_token"] = response.json().get("access_token")
                    st.session_state["username"] = response.json().get("username")
                    st.session_state["role"] = response.json().get("role")
                    st.session_state["authenticated"] = True
                    time.sleep(1)
                    st.switch_page(chat_page)
                else:
                    st.warning(response.json().get("detail"))

        except requests.exceptions.Timeout:
            st.error("The server took too long to respond. Try again later.")

        except requests.exceptions.ConnectionError:
            st.error("Could not contact the server at the moment. Try again later.")

st.divider()

st.markdown("Don't have an account?")

if st.button("Signup", type="primary"):
    st.switch_page(signup_page)
