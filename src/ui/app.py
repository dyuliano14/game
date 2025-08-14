import os, json, time, re
import streamlit as st
from .init_state import ensure_state_initialized
from .components import render_fill_blanks, render_pdf_uploader, render_mission_map

# Fallback simples caso ainda não haja missões
class SimpleLevel:
    def __init__(self, data=None):
        if data:
            self.text_segments = data.get("text_segments", [])
            self.keywords = data.get("keywords", [])
            self.options = data.get("options", [])
        else:
            self.text_segments = ["A", " dispõe sobre a", "."]
            self.keywords = ["Lei", "matéria"]
            self.options = ["Lei", "matéria", "ato", "decreto", "norma"]

def _current_level_from_mission():
    idx = st.session_state.get("current_mission_index")
    missions = st.session_state.get("missions", [])
    if idx is None or idx < 0 or idx >= len(missions):
        return SimpleLevel()
    return SimpleLevel(missions[idx]["data"])

def _finish_mission_and_back_to_map():
    idx = st.session_state.get("current_mission_index")
    if idx is not None:
        # marca como concluída
        prog = st.session_state.get("mission_progress", set())
        prog.add(idx)
        st.session_state.mission_progress = prog
    # retorna ao mapa
    st.session_state.page = "map"
    st.rerun()

def render_upload_page():
    ensure_state_initialized()
    render_pdf_uploader()

def render_map_page():
    ensure_state_initialized()
    st.title("Mapa de Aprendizagem")
    render_mission_map()

def _save_dir() -> str:
    base_dir = os.path.dirname(os.path.dirname(__file__))  # .../src/ui -> .../src
    d = os.path.join(base_dir, "data", "saves")
    os.makedirs(d, exist_ok=True)
    return d

def _slugify(name: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in (name or "doc")).strip("-")

def save_current_mission_progress() -> str:
    """Salva o estado da missão atual (lacunas preenchidas, progresso)."""
    ensure_state_initialized()
    idx = st.session_state.get("current_mission_index")
    if idx is None:
        return ""
    payload = {
        "timestamp": time.time(),
        "document_title": st.session_state.get("document_title"),
        "current_mission_index": idx,
        "selected_words": st.session_state.get("selected_words", {}),
        "correct_positions": list(st.session_state.get("correct_positions", set())),
        "active_blank_index": st.session_state.get("active_blank_index", 0),
    }
    path = os.path.join(_save_dir(), f"mission_{idx}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path

def save_overall_status() -> str:
    """Salva status geral do estudo (missões, concluídas, arquivo PDF)."""
    ensure_state_initialized()
    payload = {
        "timestamp": time.time(),
        "document_title": st.session_state.get("document_title"),
        "pdf_path": st.session_state.get("pdf_path"),
        "missions_count": len(st.session_state.get("missions", [])),
        "mission_progress": list(st.session_state.get("mission_progress", set())),
        "current_mission_index": st.session_state.get("current_mission_index"),
    }
    # arquivo global (retrocompatibilidade)
    global_path = os.path.join(_save_dir(), "study_status.json")
    with open(global_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    # arquivo por documento
    slug = _slugify(st.session_state.get("document_title"))
    per_doc = os.path.join(_save_dir(), f"study_status_{slug}.json")
    with open(per_doc, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return per_doc

def back_to_map_saving():
    """Botão/ação de voltar salvando missão e status."""
    save_current_mission_progress()
    save_overall_status()
    st.session_state.page = "map"
    st.rerun()

def render_main_page():
    """Tela do jogo (play)."""
    ensure_state_initialized()

    st.title("Alego-Manus — Jogo de Lacunas")

    top = st.columns(5)
    with top[0]:
        if st.button("Voltar (salvar)"):
            back_to_map_saving()
    with top[1]:
        if st.button("Salvar Missão"):
            path = save_current_mission_progress()
            if path:
                st.toast(f"Missão salva em {os.path.basename(path)}", icon="💾")
    with top[2]:
        if st.button("Salvar Status"):
            path = save_overall_status()
            st.toast(f"Status salvo em {os.path.basename(path)}", icon="📌")
    with top[3]:
        if st.button("Reiniciar Missão"):
            st.session_state.selected_words.clear()
            st.session_state.correct_positions.clear()
            st.session_state.active_blank_index = 0
            st.session_state.correct_answers = 0
            st.session_state.total_questions = 0
            st.rerun()
    with top[4]:
        if st.button("Upload"):
            st.session_state.page = "upload"
            st.rerun()

    level = _current_level_from_mission()
    render_fill_blanks(level=level, on_finish=back_to_map_saving)

    with st.expander("Debug do estado"):
        st.write("current_mission_index:", st.session_state.get("current_mission_index"))
        st.write("mission_progress:", st.session_state.get("mission_progress"))
