
import streamlit as st
import requests
from navigation import signup_page, chat_page
import time

st.set_page_config(page_title="Zoro AI | Signin")

st.title("Zoro AI | Signin to your account")

st.divider()

SIGNIN_URL = "http://localhost:8000/api/v1/auth/signin"

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
                response = requests.post(url=SIGNIN_URL, json={"username": username, "password": password})
                if response.status_code==200:
                    st.success("Signed in successfully! Redirecting to chat page...")
                    st.session_state["access_token"] = response.json().get("access_token")
                    st.session_state["username"] = response.json().get("username")
                    st.session_state["role"] = response.json().get("role")
                    st.session_state["authenticated"] = True
                    time.sleep(1.5)
                    st.switch_page(chat_page)
                else:
                    st.warning(response.json().get("detail"))
        except requests.exceptions.ConnectionError:
            st.error("Could not contact the server at the moment. Try again later.")

st.divider()

st.markdown("Don't have an account?")

if st.button("Signup", type="primary"):
    st.switch_page(signup_page)
