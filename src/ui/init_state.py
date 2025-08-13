import streamlit as st

def ensure_state_initialized():
    """Garante que o estado seja corretamente inicializado."""
    # Inicializar estruturas básicas
    if 'selected_words' not in st.session_state:
        st.session_state.selected_words = {}
        print("Inicializando selected_words como dicionário vazio")
    
    if 'correct_positions' not in st.session_state:
        st.session_state.correct_positions = set()
        print("Inicializando correct_positions como conjunto vazio")
    
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
        print("Inicializando correct_answers como 0")
    
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
        print("Inicializando total_questions como 0")
    
    # Verificar estado
    print(f"Estado atual: selected_words={st.session_state.selected_words}, correct_positions={st.session_state.correct_positions}")