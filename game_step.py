import streamlit as st

def initialize_game_state():
    """Inicializa o estado do jogo se ainda não existir."""
    if 'game_engine' not in st.session_state:
        from src.game.engine import GameEngine
        st.session_state.game_engine = GameEngine()
    
    if 'selected_words' not in st.session_state:
        st.session_state.selected_words = {}
    
    if 'correct_positions' not in st.session_state:
        st.session_state.correct_positions = set()
    
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
    
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0

def update_game_state(blank_index, word):
    """
    Atualiza o estado do jogo quando uma palavra é colocada em um espaço.
    
    Args:
        blank_index (int): Índice do espaço em branco
        word (str): Palavra selecionada
    """
    # Inicializar estado se necessário
    initialize_game_state()
    
    # Atualizar a palavra selecionada
    st.session_state.selected_words[blank_index] = word

def check_answer(blank_index, selected_word):
    """
    Verifica se a resposta está correta e atualiza o estado.
    
    Args:
        blank_index (int): Índice do espaço em branco
        selected_word (str): Palavra selecionada pelo usuário
    """
    # Garantir que o estado esteja inicializado
    initialize_game_state()
    
    current_level = st.session_state.game_engine.get_current_level()
    
    if current_level and blank_index < len(current_level.keywords):
        expected_word = current_level.keywords[blank_index]
        is_correct = selected_word.lower() == expected_word.lower()
        
        if is_correct:
            st.session_state.correct_answers += 1
            st.session_state.correct_positions.add(blank_index)
            st.toast(f"Correto! '{selected_word}' colocado com sucesso!", icon="✅")
        else:
            st.toast(f"'{selected_word}' colocado, mas não é a palavra correta.", icon="ℹ️")
        
        st.session_state.total_questions += 1