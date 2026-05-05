import streamlit as st
import streamlit.components.v1 as components
import random
import time
from animals import animals, animal_images
from ai import simulate_battle

def init_battle_state():
    if "sel1" not in st.session_state:
        st.session_state.sel1 = animals[0]
    if "sel2" not in st.session_state:
        st.session_state.sel2 = animals[1]
    if "battle_ongoing" not in st.session_state:
        st.session_state.battle_ongoing = False
    if "battle_done" not in st.session_state:
        st.session_state.battle_done = False

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

def select_random_animals():
    a1, a2 = random.sample(animals, 2)
    st.session_state.sel1 = a1
    st.session_state.sel2 = a2

def render_battle():
    init_battle_state()

    st.markdown(" ")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='mode-header'> CHOOSE YOUR FIGHTERS! </h1>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    select_col1, vs_col, select_col2 = st.columns([4, 2, 4])

    with select_col1:
        animal1 = st.selectbox("⚔️ Animal 1:", animals, key="sel1", disabled=st.session_state.battle_ongoing)
        img1 = animal_images.get(animal1)
        if img1:
            st.markdown(f"<div class='animal-img-frame'> <img src='{img1}'/> </div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='animal-img-frame'>IMAGE NOT FOUND</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='fighter-name'>{animal1.upper()}</div>", unsafe_allow_html=True)

    with vs_col:
        st.markdown("<div class='vs-col'> VS </div>", unsafe_allow_html=True)

    with select_col2:
        animal2 = st.selectbox("🛡️ Animal 2:", animals, key="sel2", disabled=st.session_state.battle_ongoing)
        img2 = animal_images.get(animal2)
        if img2:
            st.markdown(f"<div class='animal-img-frame'> <img src='{img2}'/> </div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='animal-img-frame'>IMAGE NOT FOUND</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='fighter-name'>{animal2.upper()}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    space_col1, start_col, space_col2, random_col, space_col3 = st.columns([1, 2, 0.1, 2, 1])

    with start_col:
        start_btn = st.button(
            "⚔️ BEGIN BATTLE! 🛡️",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.battle_ongoing
        )

    with random_col:
        random_btn = st.button(
            "🎲 SELECT RANDOM 🎲",
            type="secondary",
            use_container_width=True,
            on_click=select_random_animals,
            disabled=st.session_state.battle_ongoing
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    if start_btn:
        if animal1 == animal2:
            st.warning("⚠️ Please pick two different animals for an epic battle!")
            st.stop()
        st.session_state.battle_ongoing = True
        st.rerun()

    if st.session_state.battle_ongoing:
        st.markdown("<div id='battle-results-anchor'></div>", unsafe_allow_html=True)
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
                f"⚔️ <span>{animal1.upper()}</span> CHARGES FORWARD!",
                f"🛡️ <span>{animal2.upper()}</span> STANDS ITS GROUND...",
                "💥 THE GROUND TREMBLES...",
                "🔍 ANALYZING BEAST STATS...",
                "⚡ EPIC COLLISION INCOMING!",
            ]

            for cry in battle_cries:
                cry_area.markdown(f"<div class='battle-cry'>{cry}</div>", unsafe_allow_html=True)
                time.sleep(1.25)

        loading_screen.empty()
        scroll_to_section("battle-results-anchor")

        with st.spinner("💭 BEASTGPT IS DECIDING THE VICTOR..."):
            battle_result = simulate_battle(animal1, animal2)
            st.write(battle_result)

        st.session_state.battle_ongoing = False
        st.session_state.battle_done = True

        if st.session_state.battle_done:
            _, btn_col, _ = st.columns([2, 2, 2])
            with btn_col:
                if st.button("🔄 BATTLE AGAIN 🔄", type="secondary", use_container_width=True):
                    st.rerun()