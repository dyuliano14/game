import streamlit as st
import sys
import os

# Adiciona o diretório raiz ao path para importações relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.routes import route_manager

# Processamento de interações após renderização da interface
if st.session_state.get('word_selected', False):
    # Reseta a flag
    st.session_state.word_selected = False
    # Recarrega a página para mostrar a palavra selecionada
    st.rerun()

if st.session_state.get('blank_filled', False):
    # Reseta a flag
    st.session_state.blank_filled = False
    blank_index = st.session_state.get('filled_blank_index')
    
    # Verifica se a palavra está correta para este espaço
    current_level = st.session_state.game_engine.get_current_level()
    selected_word = st.session_state.selected_words[blank_index]
    expected_word = current_level.keywords[blank_index]
    
    is_correct = selected_word.lower() == expected_word.lower()
    
    if is_correct:
        st.session_state.correct_answers += 1
        st.session_state.total_questions += 1
        st.toast(f"Correto! '{selected_word}' colocado com sucesso!", icon="✅")
        
        # Marcar esta posição como corretamente preenchida
        if 'correct_positions' not in st.session_state:
            st.session_state.correct_positions = set()
        st.session_state.correct_positions.add(blank_index)
    else:
        st.toast(f"'{selected_word}' colocado, mas não parece correto.", icon="ℹ️")
        st.session_state.total_questions += 1
    
    # Recarrega a página para atualizar o próximo espaço ativo
    st.rerun()

# Verificar se a palavra foi selecionada via parâmetro de URL
if "selected_word" in st.query_params:
    selected_word = st.query_params["selected_word"]
    st.session_state.selected_word = selected_word
    # Não limpar o parâmetro ainda, precisamos dele para o JavaScript

if "blank_index" in st.query_params and "selected_word" in st.session_state:
    blank_index = int(st.query_params["blank_index"])
    word = st.session_state.selected_word
    
    # Verifica se já temos um dicionário para armazenar as palavras preenchidas
    if 'selected_words' not in st.session_state:
        st.session_state.selected_words = {}
    
    # Verifica se já temos um conjunto para posições corretas
    if 'correct_positions' not in st.session_state:
        st.session_state.correct_positions = set()
    
    # Coloca a palavra no espaço em branco clicado
    st.session_state.selected_words[blank_index] = word
    
    # Verificar se a palavra está correta para este espaço (em caso afirmativo, marcar como correta)
    if 'game_engine' in st.session_state:
        current_level = st.session_state.game_engine.get_current_level()
        if current_level and blank_index < len(current_level.keywords):
            expected_word = current_level.keywords[blank_index]
            if word.lower() == expected_word.lower():
                # Marcar esta posição como corretamente preenchida
                st.session_state.correct_positions.add(blank_index)
                st.session_state.correct_answers += 1
                st.toast(f"Correto! '{word}' colocado com sucesso!", icon="✅")
            else:
                st.toast(f"'{word}' colocado, mas não é a palavra correta para esta posição.", icon="ℹ️")
        
        st.session_state.total_questions += 1
    
    # Limpa a seleção de palavra
    st.session_state.selected_word = None
    
    # Limpar parâmetros de URL após processar
    st.query_params.clear()
    
    # Recarregar para mostrar a mudança
    st.rerun()

if __name__ == "__main__":
    route_manager()