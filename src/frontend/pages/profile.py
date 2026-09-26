
from navigation import signin_page
from src.backend.constants.config import secrets
import requests
import streamlit as st
import time


st.set_page_config(page_title="Zoro AI | Profile")

st.title("Zoro AI | Profile")

st.divider()

PROFILE_URL = f"{secrets.BACKEND_BASE_URL}/users/me"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('access_token')}"}

def get_profile():
    response = requests.get(url=PROFILE_URL, headers=get_headers(), timeout=10)

    if response.status_code == 200:
        return response.json()

    if response.status_code == 401:
        st.session_state["access_token"] = None
        st.session_state["authenticated"] = False

        st.warning("Your session has expired. Please signin again.")
        st.switch_page(signin_page)

    return None


try:
    profile = get_profile()

    if profile:

        st.table({
            "Email": profile.get("email"),
            "Username": profile.get("username"),
            "Role": profile.get("role"),
            "Account Created": profile.get("created_at")[0:10]
        })

        if not st.session_state.get("editing_profile", False):

            if st.button("Update Profile", use_container_width=True):
                st.session_state["editing_profile"] = True
                st.rerun()

        else:

            st.divider()

            email = st.text_input("Email (Optional)", value=profile.get("email"), max_chars=254)
            username = st.text_input("Username (Optional)", value=profile.get("username"), max_chars=24)
            new_password = st.text_input("New Password (Optional)", type="password", max_chars=64)
            current_password = st.text_input("Current Password *", type="password", max_chars=64)

            st.info("Updating the profile will expire the current session and you will have to signin again.")

            if st.button("Save Changes", use_container_width=True, type="primary"):
                if not username or len(username) < 4:
                    st.warning("Username must be at least 4 characters.")
                elif new_password and len(new_password) < 8:
                    st.warning("New password must be at least 8 characters.")
                elif not current_password or len(current_password) < 8:
                    st.warning("Current password must be at least 8 characters.")
                else:

                    body = {}

                    if email != profile.get("email"):
                        body["email"] = email
                    if username != profile.get("username"):
                        body["username"] = username
                    if new_password:
                        body["new_password"] = new_password

                    if not body:
                        st.warning("No changes were made.")

                    else:
                        body["current_password"] = current_password

                        try:
                            with st.spinner("Updating profile. Please wait..."):
                                res = requests.patch(
                                    url=PROFILE_URL, headers=get_headers(), json=body, timeout=10
                                )

                            if res.status_code == 200:
                                st.success("Profile updated successfully! Logging out and redirecting to Signin page...")
                                time.sleep(1)
                                st.session_state.clear()
                                st.switch_page(signin_page)
                            else:
                                try:
                                    st.warning(res.json().get("detail"))
                                except requests.exceptions.JSONDecodeError:
                                    st.error("Failed to update profile.")

                        except requests.exceptions.Timeout:
                            st.error("The server took too long to respond. Try again later.")
                        except requests.exceptions.ConnectionError:
                            st.error("Could not contact the server at the moment. Try again later.")

            if st.button("Cancel", use_container_width=True):
                st.session_state["editing_profile"] = False
                st.rerun()

except requests.exceptions.Timeout:
    st.error("The server took too long to respond. Try again later.")
except requests.exceptions.ConnectionError:
    st.error("Could not contact the server at the moment. Try again later.")
