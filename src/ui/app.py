import streamlit as st
import os
from src.extractor.pdf_extractor import PDFExtractor
from src.game.game_state import initialize_game_state
from src.ui.components import render_keyword_buttons, render_progress_bar

def load_css_and_js():
    """Carrega estilos CSS personalizados e JavaScript a partir de arquivos externos."""
    # Criar a pasta static se não existir
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    # Carregar CSS
    css_file = os.path.join(static_dir, 'styles.css')
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"Arquivo CSS não encontrado: {css_file}")
    
    # Carregar JavaScript
    js_file = os.path.join(static_dir, 'game_interaction.js')
    if os.path.exists(js_file):
        with open(js_file, 'r', encoding='utf-8') as f:
            st.components.v1.html(f'<script>{f.read()}</script>', height=0)
    else:
        st.warning(f"Arquivo JavaScript não encontrado: {js_file}")

def format_text_with_blanks(text, keywords, selected_words=None):
    """
    Formata o texto substituindo palavras-chave por espaços em branco.
    """
    if selected_words is None:
        selected_words = {}
    
    # Log para depuração
    print(f"Selected words: {selected_words}")
    print(f"Correct positions: {st.session_state.get('correct_positions', set())}")
    
    # Inicializa o conjunto de posições corretas se necessário
    if 'correct_positions' not in st.session_state:
        st.session_state.correct_positions = set()
    
    # Encontrar o próximo índice de espaço vazio e destacá-lo
    next_blank_idx = None
    for i in range(len(keywords)):
        # Pulamos posições já marcadas como corretas E aquelas já preenchidas
        if i not in st.session_state.correct_positions and i not in selected_words:
            next_blank_idx = i
            break
    
    # Log para depuração
    print(f"Next blank index: {next_blank_idx}")
    
    # Encontrar todas as posições das palavras-chave no texto
    replacements = []
    for idx, keyword in enumerate(keywords):
        # Encontrar todas as ocorrências da palavra no texto
        start_pos = 0
        while start_pos < len(text):
            pos = text.find(keyword, start_pos)
            if pos == -1:
                break
            
            # Verificar se a palavra não está dentro de outra palavra
            is_standalone = True
            
            # Verificar se há espaço ou pontuação antes
            if pos > 0 and text[pos-1].isalpha():
                is_standalone = False
            
            # Verificar se há espaço ou pontuação depois
            end_pos = pos + len(keyword)
            if end_pos < len(text) and text[end_pos].isalpha():
                is_standalone = False
            
            if is_standalone:
                if idx in selected_words:
                    # MUDANÇA AQUI: Verificar se esta posição está marcada como correta
                    if idx in st.session_state.correct_positions:
                        # Mostrar com estilo de sucesso (marca de verificação)
                        replacement = f'<span class="filled-word correct">✓ {selected_words[idx]}</span>'
                    else:
                        # Mostrar normalmente
                        replacement = f'<span class="filled-word">{selected_words[idx]}</span>'
                else:
                    # Caso contrário, mostrar espaço em branco com ID único
                    min_width = max(len(keyword) * 8, 50)
                    
                    # MUDANÇA AQUI: Adicionar classe 'active' APENAS no próximo espaço a ser preenchido
                    # E verificar EXPLICITAMENTE que não é uma posição já correta
                    active_class = ""
                    if idx == next_blank_idx and idx not in st.session_state.correct_positions:
                        active_class = " active"
                        print(f"Setting active class for index {idx}")
                    
                    # Espaço em branco clicável (sem onclick inline)
                    replacement = f'<span class="blank-word{active_class}" data-index="{idx}" id="blank_{idx}" style="min-width: {min_width}px; cursor: pointer;">Clique para preencher</span>'

                # Guardar a posição e o texto de substituição
                replacements.append((pos, len(keyword), replacement))
                break
            
            start_pos = pos + 1
    
    # Ordenar as substituições da direita para a esquerda para evitar problemas com índices
    replacements.sort(reverse=True)
    
    # Aplicar as substituições
    result = list(text)
    for pos, length, replacement in replacements:
        result[pos:pos+length] = replacement
    
    formatted_text = ''.join(result)
    return formatted_text

def render_main_page():
    """Renderiza a página principal do aplicativo."""
    st.title("Jogo de Aprendizado Legislativo")
    
    # Inicializa o estado do jogo
    initialize_game_state()
    
    # Carregar CSS e JavaScript
    load_css_and_js()
    
    # Obter nível atual
    current_level = st.session_state.game_engine.get_current_level()
    
    if current_level:
        st.header("Artigo em Estudo")
        
        # Exibir texto com espaços em branco
        formatted_text = format_text_with_blanks(
            current_level.article_text, 
            current_level.keywords,
            st.session_state.selected_words
        )
        st.markdown(formatted_text, unsafe_allow_html=True)
        
        # Exibir palavras-chave como botões
        st.subheader("Palavras disponíveis")
        render_keyword_buttons(current_level.keywords)
        
        # Exibir barra de progresso
        st.subheader("Seu progresso")
        render_progress_bar(
            st.session_state.correct_answers,
            st.session_state.total_questions
        )
    else:
        st.error("Nenhum nível de jogo disponível.")
