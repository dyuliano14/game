import streamlit as st
import os
from src.extractor.pdf_extractor import PDFExtractor

def initialize_game_state():
    """Inicializa o estado do jogo se ainda não existir."""
    if 'game_engine' not in st.session_state:
        from src.game.engine import GameEngine
        
        # Definir um caminho padrão para o PDF de exemplo
        # Substitua pelo caminho real do seu PDF
        default_pdf_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "data",
            "sample.pdf"
        )
        
        # Verificar se o diretório e o arquivo existem
        data_dir = os.path.dirname(default_pdf_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Se o PDF não existir, criar um arquivo mock
        if not os.path.exists(default_pdf_path):
            create_mock_pdf(default_pdf_path)
            
        # Criar o extractor com o caminho do PDF
        pdf_extractor = PDFExtractor(default_pdf_path)
        
        # Agora passar o extractor para o GameEngine
        st.session_state.game_engine = GameEngine(pdf_extractor)
    
    if 'selected_words' not in st.session_state:
        st.session_state.selected_words = {}
    
    if 'correct_positions' not in st.session_state:
        st.session_state.correct_positions = set()
    
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
    
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0

def create_mock_pdf(filepath):
    """Cria um arquivo PDF mock para testes."""
    # Criar um arquivo de texto simples para teste
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("Este é um arquivo de teste para o jogo.\n")
        f.write("A Assembleia Legislativa do Estado de Goiás, com sede na Capital do Estado, funciona normalmente no Palácio Maguito Vilela.\n")
        f.write("§ 1º Havendo motivo relevante ou de força maior, a Assembleia Legislativa poderá, por deliberação da Mesa e ad referendum da maioria absoluta dos seus Membros, reunir-se em outro edifício ou em ponto diverso no território estadual, observado o que dispõe este Regimento.\n")
        f.write("§ 2º No Plenário do Palácio Maguito Vilela não se realizarão atos estranhos à função da Assembleia Legislativa.\n")
        f.write("CAPÍTULO II\nDA HABILITAÇÃO PARA POSSE\n")

def update_game_state(blank_index, word):
    """Atualiza o estado do jogo quando uma palavra é colocada."""
    # Inicializar estruturas de dados se não existirem
    if 'selected_words' not in st.session_state:
        st.session_state.selected_words = {}
        
    if 'correct_positions' not in st.session_state:
        st.session_state.correct_positions = set()
    
    # CRUCIAL: Garantir que a palavra seja armazenada
    st.session_state.selected_words[blank_index] = word
    print(f"update_game_state: palavra '{word}' armazenada no índice {blank_index}")
    print(f"Estado após armazenamento: {st.session_state.selected_words}")
    
    # Verificar se a palavra está correta
    current_level = st.session_state.game_engine.get_current_level()
    
    if current_level and blank_index < len(current_level.keywords):
        expected_word = current_level.keywords[blank_index]
        is_correct = word.lower() == expected_word.lower()
        
        if is_correct:
            # CRUCIAL: Registrar posição como correta
            st.session_state.correct_positions.add(blank_index)
            print(f"Posição {blank_index} marcada como correta!")
            print(f"Posições corretas: {st.session_state.correct_positions}")
            
            st.session_state.correct_answers += 1
            st.toast(f"Correto! '{word}' colocado com sucesso!", icon="✅")
        else:
            st.toast(f"'{word}' colocado, mas não é a palavra correta.", icon="ℹ️")
            
        st.session_state.total_questions += 1

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