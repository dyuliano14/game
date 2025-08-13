import streamlit as st
from src.ui.event_handlers import process_events
from src.ui.init_state import ensure_state_initialized

def render_settings_page():
    """Renderiza a página de configurações."""
    st.title("Configurações")
    st.write("Esta é a página de configurações.")
    
    if st.button("Voltar para o Jogo"):
        st.session_state.page = "main"
        st.rerun()

def render_about_page():
    """Renderiza a página Sobre."""
    st.title("Sobre o Jogo")
    st.write("Este é um jogo educacional para aprender legislação.")
    
    if st.button("Voltar para o Jogo"):
        st.session_state.page = "main"
        st.rerun()

def process_events():
    """Processa todos os eventos da aplicação."""
    # Importação tardia para evitar ciclo
    from src.ui.event_handlers import process_events as handle_events
    handle_events()

def route_manager():
    """
    Gerencia as diferentes "rotas" ou páginas da aplicação.
    No Streamlit, usamos uma abordagem baseada em estado para simular rotas.
    """
    # Garantir que o estado seja inicializado corretamente
    ensure_state_initialized()
    
    # Inicializar estado se não existir
    if "page" not in st.session_state:
        st.session_state.page = "main"
    
    # Processar eventos e parâmetros de URL antes de renderizar a página
    process_events()
    
    # Renderizar a página apropriada baseado no estado
    if st.session_state.page == "main":
        # Importação tardia para evitar ciclo
        from src.ui.app import render_main_page
        render_main_page()
    elif st.session_state.page == "settings":
        render_settings_page()
    elif st.session_state.page == "about":
        render_about_page()
    else:
        # Importação tardia para evitar ciclo
        from src.ui.app import render_main_page
        render_main_page()  # Fallback para página principal