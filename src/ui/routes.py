import streamlit as st
from src.ui.init_state import ensure_state_initialized
from src.ui.event_handlers import process_events as handle_events

def route_manager():
    ensure_state_initialized()
    handle_events()

    # Página padrão
    if "page" not in st.session_state:
        st.session_state.page = "upload"

    # Import tardio para evitar ciclos e render conforme a página atual
    page = st.session_state.page
    if page == "upload":
        from src.ui.app import render_upload_page
        render_upload_page()
    elif page == "map":
        from src.ui.app import render_map_page
        render_map_page()
    elif page == "play":  # <- importante: reconhecer play
        from src.ui.app import render_main_page
        render_main_page()
    else:
        from src.ui.app import render_upload_page
        render_upload_page()