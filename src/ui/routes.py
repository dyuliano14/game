import streamlit as st
from src.ui.init_state import ensure_state_initialized
from src.ui.event_handlers import process_events as handle_events

def route_manager():
    ensure_state_initialized()
    handle_events()

    # Default de página
    if "page" not in st.session_state:
        st.session_state.page = "upload"  # começa pelo upload
    # Se já tem missões mas está em upload, ir para o mapa
    if st.session_state.page == "upload" and st.session_state.get("missions"):
        st.session_state.page = "map"

    # Import tardio para evitar ciclos
    from src.ui.app import render_main_page, render_upload_page, render_map_page

    if st.session_state.page == "main":
        render_main_page()
    elif st.session_state.page == "upload":
        render_upload_page()
    elif st.session_state.page == "map":
        render_map_page()
    else:
        render_map_page()