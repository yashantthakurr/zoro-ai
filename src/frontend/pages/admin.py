
from utils.config import API_BASE_URL
from typing import Dict, List, Optional
from utils.menu import (
    menu,
    redirect_if_not_admin,
    redirect_if_unauthenticated
)
from utils.navigation import (
    signin_page,
    chat_page
)
import requests
import streamlit as st
import time

st.set_page_config(page_title="Zoro AI | Admin", page_icon="⚔️", layout="centered")

redirect_if_unauthenticated()
redirect_if_not_admin()
menu()

st.title("Zoro AI | Admin Dashboard")
st.divider()

USERS_URL = f"{API_BASE_URL}/users"

def auth_headers() -> Dict[str, str]:
    return {"Authorization": f"Bearer {st.session_state.get('access_token')}"}

def handle_unauthorized(status_code: int) -> bool:
    if status_code == 401:
        st.session_state.clear()
        st.warning("Your session has expired. Please signin again.")
        st.switch_page(signin_page)
        return True
    if status_code == 403:
        st.warning("Your admin access is no longer valid. Redirecting...")
        time.sleep(1)
        st.switch_page(chat_page)
        return True
    return False

def fetch_all_users() -> Optional[List[Dict]]:
    try:
        resp = requests.get(f"{USERS_URL}/", headers=auth_headers(), timeout=10)
    except requests.exceptions.Timeout:
        st.error("The server took too long to respond. Try again later.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Could not contact the server at the moment. Try again later.")
        return None

    if handle_unauthorized(resp.status_code):
        st.stop()

    if resp.status_code == 200:
        return resp.json()

    st.error("Couldn't load the user list.")
    return None

def fetch_user(user_id: int) -> Optional[Dict]:
    try:
        resp = requests.get(f"{USERS_URL}/{user_id}", headers=auth_headers(), timeout=10)
    except requests.exceptions.RequestException:
        st.error("Couldn't reach the server. Try again later.")
        return None

    if handle_unauthorized(resp.status_code):
        st.stop()

    if resp.status_code == 200:
        return resp.json()
    if resp.status_code == 404:
        st.warning("That user no longer exists.")
        return None

    st.error("Couldn't load that user.")
    return None

users = fetch_all_users()

if users is not None:

    st.subheader(f"All Users ({len(users)})")

    st.dataframe(
        [
            {
                "ID": u["id"],
                "Username": u["username"],
                "Email": u["email"],
                "Role": u["role"],
                "Created": u["created_at"][0:10],
            }
            for u in users
        ],
        width="stretch",
        hide_index=True,
    )

    st.divider()
    st.subheader("Manage a User")

    options = {f'{u["id"]} - {u["username"]} ({u["role"]})': u["id"] for u in users}
    selected_label = st.selectbox("Select a user", options=list(options.keys()))
    selected_id = options[selected_label]

    user = fetch_user(selected_id)

    if user:

        is_self = user["username"] == st.session_state.get("username")
        if is_self:
            st.info("This is your own account — manage it from the Profile page instead.")

        st.write(f"**Role:** {user['role']}  |  **Joined:** {user['created_at'][0:10]}")

        with st.form(key=f"edit_user_{user['id']}"):
            email = st.text_input("Email", value=user["email"], max_chars=254)
            username = st.text_input("Username", value=user["username"], max_chars=24)
            new_password = st.text_input("New Password (leave blank to keep unchanged)", type="password", max_chars=64)
            submitted = st.form_submit_button("Save Changes", type="primary", width="stretch", disabled=is_self)

        if submitted:
            if not username or len(username) < 4:
                st.warning("Username must be at least 4 characters.")
            elif new_password and len(new_password) < 8:
                st.warning("New password must be at least 8 characters.")
            else:
                body = {}
                if email != user["email"]:
                    body["email"] = email
                if username != user["username"]:
                    body["username"] = username
                if new_password:
                    body["new_password"] = new_password
                if not body:
                    st.warning("No changes were made.")
                else:
                    try:
                        res = requests.patch(
                            f"{USERS_URL}/{user['id']}",
                            headers=auth_headers(),
                            json=body,
                            timeout=10,
                        )
                    except requests.exceptions.RequestException:
                        st.error("Couldn't reach the server. Try again later.")
                    else:
                        if handle_unauthorized(res.status_code):
                            st.stop()
                        elif res.status_code == 200:
                            st.success("User updated successfully.")
                            time.sleep(1)
                            st.rerun()
                        elif res.status_code == 409:
                            st.warning(res.json().get("detail"))
                        elif res.status_code == 404:
                            st.warning("That user no longer exists.")
                        else:
                            st.error("Failed to update user.")

        st.divider()
        st.markdown("**Danger Zone**")

        confirm = st.checkbox(f"I understand this will permanently delete '{user['username']}'.", disabled=is_self)
        if st.button("Delete User", type="primary", width="stretch", disabled=is_self or not confirm):
            try:
                res = requests.delete(f"{USERS_URL}/{user['id']}", headers=auth_headers(), timeout=10)
            except requests.exceptions.RequestException:
                st.error("Couldn't reach the server. Try again later.")
            else:
                if handle_unauthorized(res.status_code):
                    st.stop()
                elif res.status_code == 204:
                    st.success(f"'{user['username']}' was deleted.")
                    time.sleep(1)
                    st.rerun()
                elif res.status_code == 404:
                    st.warning("That user no longer exists.")
                else:
                    st.error("Failed to delete user.")
