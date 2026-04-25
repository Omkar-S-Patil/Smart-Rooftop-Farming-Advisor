import streamlit as st
from utils.common import set_background, load_global_css

from pages.home import home_page
from pages.crop import crop_page
from pages.fertilizer import fertilizer_page
from pages.disease import disease_page

st.set_page_config(
    page_title="Smart Rooftop Farming Advisor",
    page_icon="🌱",
    layout="wide"
)

set_background("assets/rooftop_bg.jpg")
load_global_css()

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "crop":
    crop_page()
elif st.session_state.page == "fertilizer":
    fertilizer_page()
elif st.session_state.page == "disease":
    disease_page()
