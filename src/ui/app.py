import os, json, time, re
import streamlit as st
st.set_page_config(page_title="Controlador de estudos - Jogo", page_icon="🎯", layout="wide")
from .init_state import ensure_state_initialized
from .components import render_fill_blanks, render_pdf_uploader, render_mission_map

# Modelo simples de nível (quando vier de uma missão)
class SimpleLevel:
    def __init__(self, text_segments: list[str], keywords: list[str], options: list[str]):
        self.text_segments = text_segments
        self.keywords = keywords
        self.options = options

def _current_level_from_mission() -> SimpleLevel:
    missions = st.session_state.get("missions") or []
    idx = st.session_state.get("current_mission_index")
    if not missions or idx is None or idx < 0 or idx >= len(missions):
        # fallback simples
        return SimpleLevel(["Texto de exemplo com "], ["lacunas"], ["lacunas", "exemplo"])
    m = missions[idx]
    data = m.get("data", {})
    text_segments = data.get("text_segments") or []
    keywords = data.get("keywords") or []
    options = data.get("options") or keywords[:]  # fallback
    return SimpleLevel(text_segments, keywords, options)

def _finish_mission_and_back_to_map():
    if "mission_progress" not in st.session_state:
        st.session_state.mission_progress = set()
    idx = st.session_state.get("current_mission_index")
    if idx is not None:
        st.session_state.mission_progress.add(idx)
    st.session_state.page = "map"
    st.rerun()

def render_upload_page():
    ensure_state_initialized()
    st.title("Jogo de Aprender")
    render_pdf_uploader()

def render_map_page():
    ensure_state_initialized()
    st.title("Mapa de Missões")
    # Um único botão de voltar (key única)
    if st.button("Voltar para Upload", key="btn_back_upload_top"):
        st.session_state.page = "upload"
        st.rerun()
    # Esconde o botão interno do componente
    render_mission_map(show_back_button=False)

def render_main_page():
    ensure_state_initialized()
    level = _current_level_from_mission()

    # Ações superiores
    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("Voltar (salvar)", key="btn_back_save"):
            _finish_mission_and_back_to_map()
    with a2:
        if st.button("Reiniciar Missão", key="btn_reset_mission"):
            st.session_state.selected_words.clear()
            st.session_state.correct_positions.clear()
            st.session_state.active_blank_index = 0
            st.session_state.correct_answers = 0
            st.session_state.total_questions = 0
            st.rerun()
    with a3:
        if st.button("Upload", key="btn_go_upload_from_play"):
            st.session_state.page = "upload"
            st.rerun()

    # Layout 2 colunas
    left, right = st.columns([2, 1])
    with left:
        st.subheader("Artigo em estudo")
        # Mostra o texto com lacunas simples (componente existente)
        render_fill_blanks(level=level, on_finish=_finish_mission_and_back_to_map)
    with right:
        st.subheader("Seu progresso")
        total = len(level.keywords) or 1
        correct = len(st.session_state.correct_positions)
        st.progress(correct / total, text=f"{correct}/{total}")
