
from src.backend.constants.config import secrets
from utils.menu import redirect_if_authenticated
from utils.navigation import signin_page
import requests
import streamlit as st
import time

st.set_page_config(page_title="Zoro AI | Signup")

st.title("Zoro AI | Create new account")

st.divider()

SIGNUP_URL = f"{secrets.BACKEND_BASE_URL}/auth/signup"

email = st.text_input(label="E-mail", type="email", max_chars=254)
username = st.text_input(label="Username", max_chars=24)
password = st.text_input(label="Password", type="password", max_chars=64)

if st.button("Signup", use_container_width=True, type="primary"):
    if not email or not username or not password:
        st.warning("All fields are required.")
    elif len(username) < 4:
        st.warning("Username must be of 4 characters.")
    elif len(password) < 8:
        st.warning("Password must be of 8 characters.")
    else:
        try:
            with st.spinner("Creating account. Please wait..."):
                response = requests.post(url=SIGNUP_URL, json={"email": email, "username": username, "password": password}, timeout=10)
                if response.status_code==201:
                    st.success("Signed up successfully! Redirecting to Signin page...")
                    time.sleep(1)
                    st.switch_page(signin_page)
                else:
                    st.warning(response.json().get("detail"))

        except requests.exceptions.Timeout:
            st.error("The server took too long to respond. Try again later.")

        except requests.exceptions.ConnectionError:
            st.error("Could not contact the server at the moment. Try again later.")

st.divider()

st.markdown("Already have an account?")

if st.button("Signin", type="primary"):
    st.switch_page(signin_page)
