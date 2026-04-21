import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "beastgptv2_logo.png"

# Streamlit App Configuration
st.set_page_config(page_title="BeastGPT", page_icon=str(LOGO_PATH), layout="wide")

# Load CSS
def load_css(filename: str = "styles.css") -> None:
    css_path = BASE_DIR / filename
    if not css_path.exists():
        st.error(f"Missing CSS file: {css_path}")
        st.stop()
    css = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
 
load_css("styles.css")

# BeastGPT Header
def render_header():
    left, right = st.columns([6, 3])

    # Left Column
    logo_col, text_col = left.columns([1, 8])
    logo_col.image(str(LOGO_PATH), width=90)
    title_html = """
    <div id="header-left">
        <h1> BeastGPT </h1>
        <div> AI-POWERED ANIMAL BATTLE SIMULATOR <div/>
    </div>
    """
    text_col.markdown(title_html, unsafe_allow_html=True)

    # Right Column
    mode = right.radio(" ", ("BATTLE MODE", "CHAT MODE"), index=0, horizontal=True, key="mode_toggle")
    return mode

# Render Header
mode = render_header()

# Render Page
if mode == "BATTLE MODE":
    st.markdown(" ")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='mode-header'> CHOOSE YOUR FIGHTERS! </h1>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("#")
    st.write("Battle page - content coming soon.")
else:
    st.markdown(" ")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='mode-header'> DESCRIBE YOUR BATTLE! </h1>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("#")
    st.write("Chat page - content coming soon.")


