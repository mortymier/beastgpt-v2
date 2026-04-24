import streamlit as st
import streamlit.components.v1 as components
import random
import time
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

# Render Page (BATTLE MODE)
if mode == "BATTLE MODE":
    st.markdown(" ")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='mode-header'> CHOOSE YOUR FIGHTERS! </h1>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if "sel1" not in st.session_state:
        st.session_state.sel1 = animals[0]
    if "sel2" not in st.session_state:
        st.session_state.sel2 = animals[1]

    def scroll_to_section(anchor_id: str):
        components.html(
            f"""
            <script>
                window.parent.document.
                getElementById('{anchor_id}').
                scrollIntoView({{behavior: 'smooth', block: 'start'}});
            </script>
            """,
            height=0,
        )

    def play_audio(url: str):
        html_code = f"""
            <audio autoplay>
                <source src="{url}" type="audio/mp3">
            </audio>
        """
        components.html(html_code, height=0, width=0)

    def select_random_animals() -> None:
        a1, a2 = random.sample(animals, 2)
        st.session_state.sel1 = a1
        st.session_state.sel2 = a2

    # Dropdown Menus
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

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Battle Mode Buttons
    space_col1, start_col, space_col2, random_col, space_col3 = st.columns([1, 2, 0.1, 2, 1])
    
    with start_col:
        start_btn = st.button("⚔️ BEGIN BATTLE! 🛡️", type="primary", use_container_width=True)

    with random_col:
        random_btn = st.button("🎲 SELECT RANDOM 🎲", type="secondary", use_container_width=True, on_click=select_random_animals)

    # Battle Results
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    if start_btn:
        st.markdown("<div id='battle-results-anchor'></div>", unsafe_allow_html=True)
        
        if animal1 == animal2:
            st.warning("⚠️ Please pick two different animals for an epic battle!")
            st.stop()
        
        loading_screen = st.empty()
        scroll_to_section("battle-results-anchor")

        play_audio("https://assets.mixkit.co/active_storage/sfx/922/922-preview.mp3")
        for num in ["3", "2", "1", "FIGHT!"]:
            with loading_screen.container():
                st.markdown(f"<div class='countdown'>{num}</div>", unsafe_allow_html=True)
            time.sleep(1)

        loading_screen.empty()
        scroll_to_section("battle-results-anchor")

        play_audio("https://assets.mixkit.co/active_storage/sfx/2780/2780-preview.mp3")
        with loading_screen.container():
            st.markdown(f"""
            <div class="fighter-slide-container">
                <div class="fighter-slide-left">
                    <div class="animal-img-frame-small"> <img src="{img1}"/> </div>
                </div>
                <div class="vs-col" style="flex: 1;">⚔️</div>
                <div class="fighter-slide-right">
                    <div class="animal-img-frame-small"> <img src="{img2}"/> </div>
                </div>
            </div> 
            """, unsafe_allow_html=True)
            
            cry_area = st.empty()
            battle_cries = [
                "SIMULATING BATTLE...",
                "SIMULATING BATTLE...",
                f"⚔️ {animal1.upper()} CHARGES FORWARD!",
                f"🛡️ {animal2.upper()} STANDS ITS GROUND...",
                "💥 THE GROUND TREMBLES...",
                "🔍 ANALYZING BEAST STATS...",
                "⚡ EPIC COLLISION INCOMING!"
            ]

            for cry in battle_cries:
                cry_area.markdown(f"<div class='fighter-name'>{cry}</div>", unsafe_allow_html=True)
                time.sleep(1.25)

        loading_screen.empty()
        scroll_to_section("battle-results-anchor")

        with st.spinner("💭 BEASTGPT IS DECIDING THE VICTOR..."):
            time.sleep(3)

# Render Page (CHAT MODE)
else:
    st.markdown(" ")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='mode-header'> DESCRIBE YOUR BATTLE! </h1>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("#")
    st.write("Chat page - content coming soon.")


