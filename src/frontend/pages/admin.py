
from utils.menu import menu, redirect_if_unauthenticated, redirect_if_not_admin
import streamlit as st
import requests

st.set_page_config(page_title="Zoro AI | Admin", page_icon="⚔️")

redirect_if_unauthenticated()
redirect_if_not_admin()
menu()

st.title("Zoro AI | Admin Dashboard")

st.divider()

