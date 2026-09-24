from typing import Dict, List
import requests
import streamlit as st

st.set_page_config(page_title="Zoro AI", page_icon="⚔️")

# Session & Token validation
username = st.session_state.get("username")
token = st.session_state.get("access_token") or st.session_state.get("token")


def handle_session_expired():
    """Clears expired credentials and offers a quick redirect to sign in."""
    st.session_state.pop("token", None)
    st.session_state.pop("access_token", None)
    st.error("⏳ Your session has expired. Please sign in again to continue.")
    if st.button("Go to Sign In", type="primary", use_container_width=True):
        try:
            st.switch_page("pages/signin.py")
        except Exception:
            st.rerun()
    st.stop()


if not username or not token:
    handle_session_expired()

API_BASE_URL = "http://localhost:8000/api/v1"
SESSION_ID = username
AUTH_HEADERS = {"Authorization": f"Bearer {token}"}

st.title("Zoro AI ⚔️")
st.caption(f"Logged in as **{username}**")
st.divider()


def load_history() -> List[Dict]:
    """Loads chat history. Detects expired token immediately on initial page load."""
    try:
        resp = requests.get(
            f"{API_BASE_URL}/chat/history/{SESSION_ID}",
            headers=AUTH_HEADERS,
            timeout=10,
        )
        if resp.status_code == 401:
            handle_session_expired()

        if resp.status_code == 200:
            data = resp.json()
            return [
                {"role": m["role"], "content": m["content"]}
                for m in data.get("messages", [])
                if m.get("content") and str(m["content"]).strip()
            ]
    except requests.RequestException:
        pass
    return []


def stream_reply(prompt: str):
    """Streams response from backend. Raises HTTPError if status >= 400."""
    with requests.post(
        f"{API_BASE_URL}/chat/send",
        headers=AUTH_HEADERS,
        json={"session_id": SESSION_ID, "message": prompt},
        stream=True,
        timeout=120,
    ) as resp:
        resp.raise_for_status()
        for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                yield chunk


# Initialize session state messages
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

with st.sidebar:
    st.subheader("Options")
    if st.button("Clear Conversation", use_container_width=True):
        try:
            requests.delete(
                f"{API_BASE_URL}/chat/history/{SESSION_ID}",
                headers=AUTH_HEADERS,
                timeout=10,
            )
        except Exception:
            pass
        st.session_state.messages = []
        st.rerun()

# Render existing messages
for message in st.session_state.messages:
    if message.get("content") and str(message["content"]).strip():
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input and streaming
if prompt := st.chat_input("Say something to Zoro..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = ""
        try:
            response = st.write_stream(stream_reply(prompt))
        except requests.exceptions.HTTPError as err:
            # Catch 401 Unauthorized specifically
            if err.response is not None and err.response.status_code == 401:
                # Remove the unanswered user prompt so it doesn't leave an orphaned message
                st.session_state.messages.pop()
                handle_session_expired()
            else:
                response = "Tch... couldn't reach the server. Try again in a moment."
                st.markdown(response)

        except requests.exceptions.ConnectionError:
            response = "Tch... couldn't reach the server. Make sure the backend is active."
            st.markdown(response)

        except requests.RequestException:
            response = "Tch... something went wrong. Try again."
            st.markdown(response)

        if not response or not str(response).strip():
            response = "Tch... couldn't hear you clearly. Ask me again."
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    