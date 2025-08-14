import streamlit as st

__all__ = [
    "ensure_state_initialized",
    "ensure_state",
    "first_unfilled_blank",
    "set_missions_in_state",
]

def ensure_state_initialized() -> None:
    # Flags básicas
    st.session_state.setdefault("word_selected", False)
    st.session_state.setdefault("blank_filled", False)

    # Estado do jogo (play)
    st.session_state.setdefault("selected_words", {})
    st.session_state.setdefault("correct_positions", set())
    st.session_state.setdefault("correct_answers", 0)
    st.session_state.setdefault("total_questions", 0)
    st.session_state.setdefault("active_blank_index", 0)

    # Documento/Missões
    st.session_state.setdefault("pdf_path", None)
    st.session_state.setdefault("document_title", None)
    st.session_state.setdefault("articles", [])
    st.session_state.setdefault("missions", [])  # cada missão tem: {title, data:{text_segments, keywords, options}}
    st.session_state.setdefault("mission_progress", set())  # índices concluídos
    st.session_state.setdefault("current_mission_index", None)

    # Engine opcional (lazy import)
    if "game_engine" not in st.session_state:
        try:
            from src.game.engine import GameEngine
            st.session_state.game_engine = GameEngine()
        except Exception as e:
            st.session_state.game_engine_error = str(e)

def ensure_state() -> None:
    ensure_state_initialized()

def first_unfilled_blank(total_blanks: int) -> int:
    sel = st.session_state.get("selected_words", {})
    for i in range(total_blanks):
        if i not in sel:
            return i
    return -1

def set_missions_in_state(missions, title: str | None, pdf_path: str | None) -> None:
    st.session_state.missions = missions or []
    st.session_state.document_title = title
    st.session_state.pdf_path = pdf_path
    st.session_state.mission_progress = set()
    st.session_state.current_mission_index = None