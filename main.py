import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "beastgptv2_logo.png"

# BeastGPT Header
st.set_page_config(page_title="BeastGPT", page_icon=str(LOGO_PATH))