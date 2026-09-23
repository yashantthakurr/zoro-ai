import requests
import streamlit as st
from typing import List, Dict

st.set_page_config(page_title="Zoro AI")

st.title("Zoro AI")

username = st.session_state.get("username")
st.text(f"Greetings, {username}!")

st.divider()

API_BASE_URL = "http://localhost:8000/api/v1"
SESSION_ID = st.session_state.get("username")


def load_history() -> List[Dict]:
    try:
        resp = requests.get(f"{API_BASE_URL}/chat/history/{SESSION_ID}", timeout=10)
        resp.raise_for_status()
        return [
            {"role": m["role"], "content": m["content"]}
            for m in resp.json()["messages"]
        ]
    except requests.RequestException:
        st.warning("Couldn't load chat history from the backend.", icon="⚠️")
        return []


def stream_reply(prompt: str):
    with requests.post(
        f"{API_BASE_URL}/chat/send",
        json={"session_id": SESSION_ID, "message": prompt},
        stream=True,
        timeout=120,
    ) as resp:
        resp.raise_for_status()
        for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                yield chunk


if "messages" not in st.session_state:
    st.session_state.messages = load_history()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.write_stream(stream_reply(prompt))
        except requests.RequestException as exc:
            response = f"[Error contacting the backend: {exc}]"
            st.error(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
