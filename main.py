import streamlit as st
from pathlib import Path
from animals import animals, animal_images

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

    # Dropdown Menus
    if "sel1" not in st.session_state:
        st.session_state.sel1 = animals[0]
    if "sel2" not in st.session_state:
        st.session_state.sel2 = animals[1]

    select_col1, vs_col, select_col2 = st.columns([4, 2, 4])

    with select_col1:
        animal1 = st.selectbox("⚔️ Animal 1:", animals, key="sel1")
        img1 = animal_images.get(animal1)
        if img1:
            st.markdown(f"<div class='animal-img-frame'> <img src='{img1}'/> </div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='animal-img-frame'>IMAGE NOT FOUND</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='fighter-name'>{animal1.upper()}</div>", unsafe_allow_html=True)

    with vs_col:
        st.markdown("<div class='vs-col'> VS </div>", unsafe_allow_html=True)

    with select_col2:
        animal2 = st.selectbox("🛡️ Animal 2:", animals, key="sel2")
        img2 = animal_images.get(animal2)
        if img2:
            st.markdown(f"<div class='animal-img-frame'> <img src='{img2}'/> </div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='animal-img-frame'>IMAGE NOT FOUND</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='fighter-name'>{animal2.upper()}</div>", unsafe_allow_html=True)

else:
    st.markdown(" ")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='mode-header'> DESCRIBE YOUR BATTLE! </h1>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("#")
    st.write("Chat page - content coming soon.")


