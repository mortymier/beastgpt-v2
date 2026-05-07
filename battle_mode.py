import streamlit as st
import random
import time
import re
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

def scroll_to_section():
    st.html(
        """
        <script>
            const element = window.parent.document.getElementById('battle-results-anchor');
            element.scrollIntoView({behavior: 'smooth', block: 'start'});
        </script>
        """,
        unsafe_allow_javascript=True,
    )

def play_audio(url: str):
    st.html(
        f"""
        <audio autoplay>
            <source src="{url}" type="audio/mp3">
        </audio>
        """
    )

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

    _, start_col, _, random_col, _ = st.columns([1, 2, 0.1, 2, 1])

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
        scroll_to_section()

        play_audio("https://assets.mixkit.co/active_storage/sfx/922/922-preview.mp3")
        for num in ["3", "2", "1", "FIGHT!"]:
            with loading_screen.container():
                st.markdown(f"<div class='countdown'>{num}</div>", unsafe_allow_html=True)
            time.sleep(1)

        loading_screen.empty()

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

        with st.spinner("💭 BEASTGPT IS DECIDING THE VICTOR..."):
            battle_result = simulate_battle(animal1, animal2)

        st.markdown("<div class='flash-overlay'></div>", unsafe_allow_html=True)
        time.sleep(0.1)
        play_audio("https://cdn.freesound.org/previews/626/626259_6303715-lq.mp3")

        winner_match = re.search(r'^WHO WINS\?\s*(?:\n\s*)?([A-Z][A-Z &-]*)\s*$', battle_result, re.MULTILINE)
        winner = winner_match.group(1).strip() if winner_match else None

        sections = battle_result.split('\n\n')
        story_paragraphs = []
        table_block = None
        in_stats = False

        for section in sections:
            stripped = section.strip()
            if '|Trait' in stripped or '|---' in stripped or (stripped.startswith('|') and '|' in stripped[1:]):
                table_block = stripped
                in_stats = True
            elif 'WHO WINS' in stripped or (winner and winner in stripped and len(stripped) < 60):
                continue
            elif 'BATTLE STATS' in stripped:
                in_stats = True
            elif not in_stats and stripped and stripped not in ['BATTLE STATS']:
                story_paragraphs.append(stripped)

        scroll_to_section()

        if winner:
            st.markdown(f"""
            <div style='margin-top:-7rem;text-align:center;padding:1.5rem 0;'>
                <div style='font-family:Bebas Neue,cursive;font-size:1.2rem;color:#e8e8e8;letter-spacing:5px;margin-bottom:.5rem;'>
                    AND THE WINNER IS
                </div>
                <div class='winner-banner'>  
                    <span class='crown'>🏆</span> &nbsp; {winner} &nbsp; <span class='crown'>🏆</span>
                </div>
            </div>""", unsafe_allow_html=True)
            time.sleep(0.4)
            st.balloons()
        else:
            st.markdown("""
            <div style='text-align:center;padding:1rem 0;'>
                <div class='winner-banner'>⚔️ EPIC BATTLE CONCLUDED! ⚔️</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.session_state.battle_ongoing = False
        st.session_state.battle_done = True

        story_html = "".join(
            f"<p style='margin-bottom:1.2rem;animation:fadeSlideUp .5s {i*0.15:.2f}s ease-out both;'>{p}</p>"
            for i, p in enumerate(story_paragraphs[:4]) if p
        )

        if story_html:
            st.markdown(f"""
            <div style='margin-bottom:3rem;'>
                <div class='section-head' style='color:#cd4055;border-color:#cd4055;'>
                    📖 &nbsp; THE TALE OF BATTLE
                </div>
                <div class='story-card'>{story_html}</div>
            </div>""", unsafe_allow_html=True)
            time.sleep(0.3)

        if table_block:
            rows = [r for r in table_block.strip().split('\n') if r.strip().startswith('|')]
            header_row = rows[0] if rows else ""
            data_rows = [r for r in rows[2:] if r.strip() and '---' not in r]
    
            def parse_row(row):
                return [cell.strip() for cell in row.strip().strip('|').split('|')]
    
            headers = parse_row(header_row)

            if winner and len(headers) >= 3:
                if headers[1].upper() == winner.upper():
                    headers[1] = f"🏆 {headers[1]} (Victory)"
                    headers[2] = f"💔 {headers[2]} (Defeat)"
                elif headers[2].upper() == winner.upper():
                    headers[1] = f"💔 {headers[1]} (Defeat)"
                    headers[2] = f"🏆 {headers[2]} (Victory)"

            th_html = "".join(f"<th>{h}</th>" for h in headers)
            td_rows_html = ""
            for dr in data_rows:
                cells = parse_row(dr)
                while len(cells) < len(headers):
                    cells.append("")
                td_html = "".join(f"<td>{c}</td>" for c in cells[:len(headers)])
                td_rows_html += f"<tr>{td_html}</tr>"
    
            table_html = f"<table class='battle-table'><thead><tr>{th_html}</tr></thead><tbody>{td_rows_html}</tbody></table>"
    
            st.markdown(f"""
            <div style='margin-bottom:3rem;'>
                <div class='section-head' style='color:#4ecdc4;border-color:#4ecdc4;'>
                    ⚖️ &nbsp; BATTLE STATS
                </div>
                {table_html}
            </div>""", unsafe_allow_html=True)
        else:
            stats_start = battle_result.find('BATTLE STATS')
            if stats_start != -1:
                st.markdown(f"""
                <div class='section-head' style='color:#4ecdc4;border-color:#4ecdc4;'>
                    ⚔️ &nbsp; BATTLE STATS
                </div>""", unsafe_allow_html=True)
                st.markdown(battle_result[stats_start + len('BATTLE STATS'):])
 
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.battle_done:
            _, btn_col, _ = st.columns([2, 2, 2])
            with btn_col:
                if st.button("🔄 BATTLE AGAIN 🔄", type="secondary", use_container_width=True):
                    st.rerun()