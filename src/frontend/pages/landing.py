
from utils.menu import redirect_if_authenticated
import streamlit as st

def landing_page():

    st.set_page_config(
        page_title="Zoro AI",
        page_icon="⚔️️",
        layout="centered",
    )

    st.markdown(
        """
        <style>
        .main {
            background: #0e0e0e;
        }

        .zoro-title {
            text-align: center;
            font-size: 64px;
            font-weight: 800;
            margin-top: 80px;
            margin-bottom: 5px;
        }

        .zoro-subtitle {
            text-align: center;
            font-size: 22px;
            color: #bdbdbd;
            margin-bottom: 30px;
        }

        .zoro-text {
            text-align: center;
            font-size: 17px;
            color: #999;
            max-width: 600px;
            margin: auto;
        }

        .quote {
            text-align: center;
            margin-top: 45px;
            font-size: 18px;
            color: #aaa;
            font-style: italic;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="zoro-title">Zoro AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="zoro-subtitle">Lost? Zoro probably is too.</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        """
        <div class="zoro-text">
            A small AI chatbot made by a One Piece fan,
            for anyone who enjoys One Piece and wants a simple
            place to chat, ask questions and mess around with AI.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button(
                "🏴‍☠️ Try Zoro AI for Free",
                use_container_width=True,
        ):
            st.switch_page("pages/signin.py")

    st.markdown(
        """
        <div class="quote">
            "Nothing happened." — Roronoa Zoro
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")

    st.divider()

    st.markdown(
        """
        <div style="text-align:center; color:#777;">
            Built with ☕ + Python + FastAPI + a little One Piece obsession
        </div>
        """,
        unsafe_allow_html=True,
    )

redirect_if_authenticated()
landing_page()
