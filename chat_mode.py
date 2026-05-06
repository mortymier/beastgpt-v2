import streamlit as st
import html
import re
from pathlib import Path
from ai import simulate_chat_battle

LOGO_PATH = Path(__file__).resolve().parent / "beastgptv2_logo.png"
BEAST_LOGO_BYTES = LOGO_PATH.read_bytes() if LOGO_PATH.exists() else None

def init_chat_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_phase" not in st.session_state:
        st.session_state.chat_phase = "scenario"

def render_chat():
    init_chat_state()

    st.markdown(" ")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='mode-header'> DESCRIBE YOUR BATTLE! </h1>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.chat_history:
        _, center, _ = st.columns([1, 6, 1])
        with center:
            st.markdown("""
                <div style="text-align:center; line-height:2; letter-spacing:1px; margin-bottom: 2rem">
                    💬 Tell <span style="color:crimson">BeastGPT</span> about your epic animal battle! <br>
                    ⚔️ Which <span style="color:orange">two animals</span>  are going to be fighting? <br>
                    ⛅ What is the  <span style="color:gold">weather and terrain</span> during the battle? <br>
                    <span style="color:gray"> Example: Alligator vs Anaconda in a riverbank while raining. </span>
                </div>""", unsafe_allow_html=True)

    for message in st.session_state.chat_history:
        avatar = BEAST_LOGO_BYTES if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "user":
                st.markdown(message["content"])
            elif message["role"] == "assistant" and "WHO WINS" in message["content"].upper():
                render_battle_result(message["content"])
            else:
                st.markdown(message["content"])

    user_input = st.chat_input("Describe your battle scenario...", key="chat_input")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("assistant", avatar=BEAST_LOGO_BYTES):
            full_response = ""
            placeholder = st.empty()

            for chunk in simulate_chat_battle(user_input, st.session_state.chat_history):
                full_response += chunk
                placeholder.markdown(full_response)

            st.session_state.chat_history.append({"role": "assistant", "content": full_response})

        st.rerun()

    # Clear chat button — only show if there's history
    if st.session_state.chat_history:
        _, _, right = st.columns([2, 2, 1])
        with right:
            if st.button("🗑️ CLEAR CHAT 🗑️", type="secondary", key="clear_chat"):
                st.session_state.chat_history = []
                st.session_state.chat_phase = "scenario"
                st.rerun()


def render_battle_result(result_text: str):
    def normalize_text(value: str) -> str:
        if not value:
            return ""
        cleaned = value.strip()
        cleaned = re.sub(r"^[#>\-\*\s]+", "", cleaned)
        cleaned = cleaned.replace("`", "").replace("*", "").replace("_", "").replace("**", "")
        return cleaned.upper()

    normalized_result = normalize_text(result_text)
    winner_match = re.search(r'WHO WINS\?\s*([A-Z0-9 &-]+)', normalized_result)
    winner = winner_match.group(1).strip() if winner_match else None
    winner_norm = normalize_text(winner) if winner else None

    sections = result_text.split('\n\n')
    preamble_paragraphs = [] 
    story_paragraphs = []
    table_block = None
    in_stats = False
    past_winner_line = False

    for section in sections:
        stripped = section.strip()
        if '|Trait' in stripped or '|---' in stripped or (stripped.startswith('|') and '|' in stripped[1:]):
            table_block = stripped
            in_stats = True
        elif 'WHO WINS' in stripped or (winner and winner in stripped and len(stripped) < 60):
            past_winner_line = True
            continue
        elif 'BATTLE STATS' in stripped:
            in_stats = True
        elif not past_winner_line and not in_stats and stripped:  
            preamble_paragraphs.append(stripped)
        elif past_winner_line and not in_stats and stripped and stripped not in ['BATTLE STATS']:
            story_paragraphs.append(stripped)

    if preamble_paragraphs or winner or story_paragraphs:
        combined_md = ""
        if preamble_paragraphs:
            combined_md += "\n\n".join(preamble_paragraphs) + "\n\n" 
        if winner:
            combined_md += f"**WHO WINS? {winner}**\n\n"
        if story_paragraphs:
            combined_md += "\n\n".join(story_paragraphs[:4])
        st.markdown(combined_md)

    if table_block:
        rows = [r for r in table_block.strip().split('\n') if r.strip().startswith('|')]
        if rows:
            header_row = rows[0]
            data_rows = [r for r in rows[2:] if r.strip() and '---' not in r]

            def parse_row(row):
                return [cell.strip() for cell in row.strip().strip('|').split('|')]

            headers = parse_row(header_row)

            if winner_norm and len(headers) >= 3:
                left_header_norm = normalize_text(headers[1])
                right_header_norm = normalize_text(headers[2])

                if left_header_norm == winner_norm:
                    headers[1] = f"🏆 {headers[1]} (Victory)"
                    headers[2] = f"💔 {headers[2]} (Defeat)"
                elif right_header_norm == winner_norm:
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
            <div style='margin-top:1.5rem;'>
                <div style='font-size: 1.1rem; font-weight: 700; color: #4ecdc4; margin-bottom: 1rem; letter-spacing: 1px;'>
                    ⚖️ BATTLE STATS
                </div>
                {table_html}
            </div>""", unsafe_allow_html=True)