
from utils.footer import get_footer
from utils.menu import redirect_if_authenticated
from utils.navigation import signin_page
import streamlit as st

st.set_page_config(page_title="Zoro AI", page_icon="⚔️", layout="centered")

redirect_if_authenticated()

with st.container(horizontal_alignment="center"):
    st.title("Zoro AI", text_alignment="center")

    st.header("Lost? Probably Zoro too...", text_alignment="center")

    st.markdown(
        "A small AI chatbot made by a One Piece fan, for anyone who enjoys "
        "One Piece and wants a simple place to chat, ask questions and mess around with AI.",
        text_alignment="center",
    )

    if st.button("🏴‍☠️ Try Zoro AI for Free", width="content"):
        st.switch_page(signin_page)

    st.markdown('*"Nothing happened." — Roronoa Zoro*', text_alignment="center")

get_footer()
