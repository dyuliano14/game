import streamlit as st

def process_events():
    """Processa todos os eventos e interações de usuário."""
    process_url_params()
    process_session_events()

def process_url_params():
    """Processa parâmetros da URL."""
    # PROBLEMA IDENTIFICADO: Verificamos os parâmetros, mas não mantemos o estado após o processamento
    
    if "selected_word" in st.query_params:
        selected_word = st.query_params["selected_word"]
        st.session_state.selected_word = selected_word
        print(f"Palavra selecionada: {selected_word}")

    if "blank_index" in st.query_params and "selected_word" in st.session_state:
        blank_index = int(st.query_params["blank_index"])
        word = st.session_state.selected_word
        
        # IMPORTANTE: Armazenar explicitamente em session_state para persistência
        if 'selected_words' not in st.session_state:
            st.session_state.selected_words = {}
        
        # Armazenar a palavra no índice especificado
        st.session_state.selected_words[blank_index] = word
        print(f"Palavra '{word}' armazenada no índice {blank_index}")
        
        # Verificar se a palavra é correta
        from src.game.game_state import update_game_state
        update_game_state(blank_index, word)
        
        # Limpar parâmetros para evitar loop
        st.query_params.clear()
        st.rerun()

def process_session_events():
    """Processa eventos guardados no session_state."""
    if st.session_state.get('word_selected', False):
        st.session_state.word_selected = False
        st.rerun()

    if st.session_state.get('blank_filled', False):
        blank_index = st.session_state.get('filled_blank_index')
        selected_word = st.session_state.selected_words[blank_index]
        
        # Importação tardia para evitar ciclo
        from src.game.game_state import check_answer
        # Delegar para a função de verificação de resposta
        check_answer(blank_index, selected_word)
        
        st.session_state.blank_filled = False
        st.rerun()

def handle_word_selection(word):
    """Função que gerencia quando uma palavra é clicada."""
    if 'selected_word' not in st.session_state:
        st.session_state.selected_word = None
    
    st.session_state.selected_word = word
    st.session_state.word_selected = True

def handle_blank_click(blank_index):
    """Função que gerencia quando um espaço em branco é clicado."""
    if 'selected_word' in st.session_state and st.session_state.selected_word:
        word = st.session_state.selected_word
        
        if 'selected_words' not in st.session_state:
            st.session_state.selected_words = {}
        
        st.session_state.selected_words[blank_index] = word
        st.session_state.blank_filled = True
        st.session_state.filled_blank_index = blank_index