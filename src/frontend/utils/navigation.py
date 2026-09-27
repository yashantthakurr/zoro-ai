
import streamlit as st

landing_page = st.Page(
    page="pages/landing.py",
    title="Zoro AI",
    default=True
)

signin_page = st.Page(
    "pages/signin.py",
    title="Signin"
)

signup_page = st.Page(
    "pages/signup.py",
    title="Signup"
)

profile_page = st.Page(
    "pages/profile.py",
    title="Profile"
)

chat_page = st.Page(
    "pages/chat.py",
    title="Chat"
)

logout_page = st.Page(
    "pages/logout.py",
    title="Logout"
)

admin_page = st.Page(
    "pages/admin.py",
    title="Dashboard"
)
