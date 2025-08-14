import streamlit as st

def format_text_with_blanks(text: str, keywords: list[str], selected_words: dict[int, str] | None = None) -> str:
    if selected_words is None:
        selected_words = {}

    if "correct_positions" not in st.session_state:
        st.session_state.correct_positions = set()

    # próximo blank que deve pulsar
    next_blank_idx = None
    for i in range(len(keywords)):
        if i not in st.session_state.correct_positions and i not in selected_words:
            next_blank_idx = i
            break

    replacements: list[tuple[int, int, str]] = []
    for idx, keyword in enumerate(keywords):
        start = 0
        while True:
            pos = text.find(keyword, start)
            if pos == -1:
                break

            # Palavra isolada
            before_ok = pos == 0 or not text[pos - 1].isalpha()
            after_ok = (pos + len(keyword) == len(text)) or not text[pos + len(keyword)].isalpha()
            if before_ok and after_ok:
                if idx in selected_words:
                    if idx in st.session_state.correct_positions:
                        repl = f'<span class="filled-word correct">✓ {selected_words[idx]}</span>'
                    else:
                        repl = f'<span class="filled-word">{selected_words[idx]}</span>'
                else:
                    min_w = max(len(keyword) * 8, 60)
                    active_cls = " active" if (idx == next_blank_idx and idx not in st.session_state.correct_positions) else ""
                    repl = f'<span class="blank-word{active_cls}" data-index="{idx}" id="blank_{idx}" style="min-width:{min_w}px;cursor:pointer;">Clique para preencher</span>'
                replacements.append((pos, len(keyword), repl))
                break
            start = pos + 1

    # aplicar substituições da direita para a esquerda
    replacements.sort(reverse=True)
    out = list(text)
    for pos, length, repl in replacements:
        out[pos:pos + length] = repl
    return "".join(out)