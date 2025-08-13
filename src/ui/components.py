import streamlit as st
from src.ui.event_handlers import handle_word_selection

def render_keyword_buttons(keywords, cols_per_row=4):
    """
    Renderiza botões para as palavras-chave.
    
    Args:
        keywords (list): Lista de palavras-chave
        cols_per_row (int): Número de colunas por linha
    """
    # Criar colunas para os botões
    num_rows = (len(keywords) + cols_per_row - 1) // cols_per_row
    for row_idx in range(num_rows):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            idx = row_idx * cols_per_row + col_idx
            if idx < len(keywords):
                keyword = keywords[idx]
                
                # Estilo especial se esta for a palavra selecionada
                is_selected = st.session_state.get('selected_word') == keyword
                button_type = "primary" if is_selected else "secondary"
                button_text = f"✓ {keyword}" if is_selected else f"👆 {keyword}"
                
                cols[col_idx].button(
                    button_text,
                    key=f"btn_{idx}_{keyword}",
                    use_container_width=True,
                    on_click=handle_word_selection,
                    args=(keyword,),
                    type=button_type
                )

def render_progress_bar(correct, total):
    """
    Renderiza uma barra de progresso.
    
    Args:
        correct (int): Número de respostas corretas
        total (int): Número total de questões
    """
    progress = 0 if total == 0 else (correct / total)
    st.progress(progress)
    st.text(f"Progresso: {correct}/{total} ({int(progress * 100)}%)")