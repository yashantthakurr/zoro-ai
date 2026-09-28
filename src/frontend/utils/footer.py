
from st_social_media_links import SocialMediaIcons
from typing import List
import streamlit as st

socialMediaLinks: List[str] = [
    "https://www.linkedin.com/in/yashant-thakur",
    "https://github.com/yashantthakurr",
    "https://www.instagram.com/yashantthakurr/"
]

custom_colors: List[str] = ["#0077b5", "#ffffff", "#E1306C"]

social_media_icons: SocialMediaIcons = SocialMediaIcons(socialMediaLinks, colors = custom_colors)

def get_footer() -> None:

    st.divider()

    st.write(
        """
                <div style = 'text-align: center; font-size: 18px; font-family: "Lato", serif'>Made by Yashant</div>
            """,
             unsafe_allow_html = True)
    social_media_icons.render()
