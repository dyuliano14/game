import os, json, hashlib
from typing import Any, Optional
import streamlit as st
import math

from .init_state import ensure_state_initialized, first_unfilled_blank

# ========== util e persistência ==========
def _base_dir() -> str:
    return os.path.dirname(os.path.dirname(__file__))  # .../src

def _upload_dir() -> str:
    d = os.path.join(_base_dir(), "data", "uploads")
    os.makedirs(d, exist_ok=True)
    return d

def _save_dir() -> str:
    d = os.path.join(_base_dir(), "data", "saves")
    os.makedirs(d, exist_ok=True)
    return d

def _index_path() -> str:
    return os.path.join(_save_dir(), "index.json")

def _load_index() -> dict:
    p = _index_path()
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_index(idx: dict) -> None:
    with open(_index_path(), "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)

def _slugify(name: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in (name or "")).strip("-")

def _seed_for(pdf_name: str, article_id: int) -> int:
    h = hashlib.sha256(f"{pdf_name}:{article_id}".encode("utf-8")).hexdigest()
    return int(h[:16], 16)

def _generate_missions_for_pdf(pdf_path: str, pdf_name: str) -> list[dict]:
    from src.extractor.pdf_extractor import (
        extract_pdf_text, split_into_articles, generate_fill_blanks_from_article
    )
    text = extract_pdf_text(pdf_path)
    articles = split_into_articles(text)
    missions: list[dict] = []
    order = 1
    for art in articles:
        seed = _seed_for(pdf_name, art["id"])
        data = generate_fill_blanks_from_article(art["text"], seed=seed)
        if not data["keywords"]:
            continue
        missions.append({
            "id": order,
            "title": art["title"],
            "data": data,
            "completed": False,
        })
        order += 1
    return missions

def _delete_pdf(fname: str) -> None:
    """Remove o PDF, o índice e o status salvo correspondente."""
    try:
        pdf_path = os.path.join(_upload_dir(), fname)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        # remover do índice
        idx = _load_index()
        if fname in idx:
            idx.pop(fname, None)
            _save_index(idx)

        # remover status salvo (se houver)
        slug = _slugify(fname)
        status_path = os.path.join(_save_dir(), f"study_status_{slug}.json")
        if os.path.exists(status_path):
            os.remove(status_path)

        # se o PDF deletado estava ativo na sessão, limpar missões
        if st.session_state.get("pdf_path") == pdf_path:
            st.session_state.missions = []
            st.session_state.document_title = None
            st.session_state.current_mission_index = None
            st.session_state.mission_progress = set()
            st.session_state.page = "upload"

        st.toast(f"🗑️ Removido: {fname}", icon="✅")
    except Exception as e:
        st.error(f"Falha ao excluir {fname}: {e}")

# ========== Upload/Listagem ==========
def render_pdf_uploader():
    """Tela de upload + listagem de PDFs com ações."""
    ensure_state_initialized()

    # Hero / cabeçalho amigável
    st.markdown(
        """
        <div class="card section">
          <h2>🧩 Gerador de missões</h2>
          <p>Continue estudando: vamos jogar e melhorar suas habilidades.<br/>
          Carregue o PDF do assunto que desejar, clique em <b>Gerar missões</b> e siga para o mapa.</p>
          <p><b>Vamos lá! 🚀</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Uploader com rótulo solicitado
    uploaded = st.file_uploader("📥 Import (PDF)", type=["pdf"])
    if uploaded:
        save_path = os.path.join(_upload_dir(), uploaded.name)
        with open(save_path, "wb") as f:
            f.write(uploaded.getbuffer())
        if st.button("🚀 Gerar missões a partir deste PDF", key="gen_from_uploader"):
            with st.spinner("Gerando missões..."):
                missions = _generate_missions_for_pdf(save_path, uploaded.name)
                from .init_state import set_missions_in_state
                set_missions_in_state(missions, title=uploaded.name, pdf_path=save_path)
                idx = _load_index()
                idx[uploaded.name] = {
                    "pdf_path": save_path,
                    "document_title": uploaded.name,
                    "missions_count": len(missions),
                }
                _save_index(idx)
            st.success(f"{len(missions)} missões criadas. 🗺️")
            st.session_state.page = "map"
            st.rerun()

    st.subheader("📚 PDFs carregados")
    files = sorted([f for f in os.listdir(_upload_dir()) if f.lower().endswith(".pdf")])
    idx = _load_index()

    if not files:
        st.info("Nenhum PDF enviado ainda. Use o campo acima para importar um arquivo. 🙂")
        return

    # Diálogo simples de confirmação de exclusão (controlado por session_state)
    to_confirm = st.session_state.get("confirm_delete_name")

    for i, fname in enumerate(files):
        pdf_path = os.path.join(_upload_dir(), fname)
        meta = idx.get(fname)

        cols = st.columns([4, 2, 2, 2, 1])  # + coluna para Excluir
        with cols[0]:
            st.write(f"• {fname}")
            if meta:
                st.caption(f"Missões: {meta.get('missions_count', 0)}")

        with cols[1]:
            if st.button("♻️ Gerar/Atualizar", key=f"gen_{i}"):
                with st.spinner("Gerando missões..."):
                    missions = _generate_missions_for_pdf(pdf_path, fname)
                    from .init_state import set_missions_in_state
                    set_missions_in_state(missions, title=fname, pdf_path=pdf_path)
                    idx[fname] = {
                        "pdf_path": pdf_path,
                        "document_title": fname,
                        "missions_count": len(missions),
                    }
                    _save_index(idx)
                st.session_state.page = "map"
                st.rerun()

        with cols[2]:
            if st.button("🗺️ Abrir mapa", key=f"open_{i}"):
                missions = _generate_missions_for_pdf(pdf_path, fname)
                from .init_state import set_missions_in_state
                set_missions_in_state(missions, title=fname, pdf_path=pdf_path)
                st.session_state.page = "map"
                st.rerun()

        with cols[3]:
            slug = _slugify(fname)
            status_path = os.path.join(_save_dir(), f"study_status_{slug}.json")
            if os.path.exists(status_path):
                if st.button("📂 Carregar status", key=f"load_{i}"):
                    try:
                        with open(status_path, "r", encoding="utf-8") as f:
                            payload = json.load(f)
                        missions = _generate_missions_for_pdf(pdf_path, fname)
                        from .init_state import set_missions_in_state
                        set_missions_in_state(missions, title=fname, pdf_path=pdf_path)
                        st.session_state.mission_progress = set(payload.get("mission_progress", []))
                        st.session_state.current_mission_index = payload.get("current_mission_index")
                        st.session_state.page = "map"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Falha ao carregar status: {e}")
            else:
                st.write("")

        with cols[4]:
            if st.button("🗑️ Excluir", key=f"del_{i}"):
                st.session_state.confirm_delete_name = fname
                st.session_state.confirm_delete_row = i
                st.rerun()

        # Bloco de confirmação inline
        if to_confirm == fname:
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("✅ Confirmar exclusão", key=f"confirm_del_{i}"):
                    _delete_pdf(fname)
                    st.session_state.pop("confirm_delete_name", None)
                    st.session_state.pop("confirm_delete_row", None)
                    st.rerun()
            with c2:
                if st.button("❌ Cancelar", key=f"cancel_del_{i}"):
                    st.session_state.pop("confirm_delete_name", None)
                    st.session_state.pop("confirm_delete_row", None)
                    st.experimental_rerun()

def _quick_save_status() -> str:
    """Salva progresso atual em JSON (por documento)."""
    slug = _slugify(st.session_state.get("document_title") or "doc")
    path = os.path.join(_save_dir(), f"study_status_{slug}.json")
    payload = {
        "mission_progress": sorted(list(st.session_state.get("mission_progress", set()))),
        "current_mission_index": st.session_state.get("current_mission_index"),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path

# ========== Mapa de Missões ==========
def render_mission_map(show_back_button: bool = False, cols: int = 5):
    """Mapa de missões com layout em zigue-zague e sequência."""
    ensure_state_initialized()
    missions = st.session_state.get("missions", [])

    top = st.columns([1, 1, 6])
    with top[0]:
        if show_back_button:
            if st.button("Voltar para Upload", key="btn_back_upload_map"):
                st.session_state.page = "upload"
                st.rerun()
    with top[1]:
        if st.button("Salvar Status", key="btn_save_status_map"):
            path = _quick_save_status()
            st.toast(f"Status salvo: {os.path.basename(path)}", icon="📌")

    if not missions:
        st.info("Nenhuma missão. Vá para Upload e gere a partir de um PDF.")
        return

    # Deduplicação leve (evita artigos repetidos no mapa)
    dedup, seen = [], set()
    for m in missions:
        key = (m.get("title"), tuple(m.get("data", {}).get("keywords", [])[:3]))
        if key not in seen:
            seen.add(key)
            dedup.append(m)
    missions = dedup

    st.header(st.session_state.get("document_title") or "Mapa de Missões")

    # Legenda simples
    st.markdown(
        '<div class="mission-legend">'
        '<span>🎯 Jogável</span><span>🏆 Concluída</span><span>🔒 Bloqueada</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    completed = st.session_state.get("mission_progress", set())
    # Próxima missão desbloqueada é a primeira não concluída
    next_playable = 0
    while next_playable in completed and next_playable < len(missions):
        next_playable += 1

    emojis_cycle = ["🎯", "🧠", "⚡", "🔥", "🛡️", "💎", "🚀"]

    total = len(missions)
    rows = math.ceil(total / cols)

    # Render em zigue-zague
    for r in range(rows):
        start = r * cols
        end = min(start + cols, total)
        chunk = list(range(start, end))

        # Alterna direção para zigue-zague
        left_to_right = (r % 2 == 0)
        ordered = chunk if left_to_right else list(reversed(chunk))

        cols_row = st.columns(cols, vertical_alignment="center")
        for i, idx in enumerate(ordered):
            m = missions[idx]
            title = m["title"]
            # rótulo curto
            short = title if len(title) <= 14 else title[:12] + "…"
            emoji = emojis_cycle[idx % len(emojis_cycle)]

            done = idx in completed
            locked = idx > max(next_playable, 0)  # bloqueia tudo após a próxima jogável
            current = (idx == next_playable and not done)

            label = f"{emoji} {idx+1}. {short}"
            if done:
                label += " 🏆"
            elif locked:
                label += " 🔒"
            else:
                label += " 🎯"

            with cols_row[i]:
                st.markdown('<div class="mission-slot">', unsafe_allow_html=True)
                if st.button(label, key=f"mission_{idx}", disabled=locked, use_container_width=True):
                    st.session_state.current_mission_index = idx
                    st.session_state.selected_words.clear()
                    st.session_state.correct_positions.clear()
                    st.session_state.active_blank_index = 0
                    st.session_state.correct_answers = 0
                    st.session_state.total_questions = 0
                    st.session_state.page = "play"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    st.caption(f"Concluídas: {len(completed)}/{len(missions)}")

# ========== Jogo: preencher lacunas ==========
def _place_selected_word(word: str, answers: list[str]) -> None:
    i = st.session_state.active_blank_index
    if i < 0 or i >= len(answers):
        return
    st.session_state.selected_words[i] = word
    if word.lower() == answers[i].lower():
        st.session_state.correct_positions.add(i)
        st.session_state.correct_answers += 1
    nxt = first_unfilled_blank(len(answers))
    if nxt >= 0:
        st.session_state.active_blank_index = nxt

def _clear_current_blank():
    i = st.session_state.active_blank_index
    st.session_state.selected_words.pop(i, None)
    st.session_state.correct_positions.discard(i)

def _clear_all():
    st.session_state.selected_words.clear()
    st.session_state.correct_positions.clear()
    st.session_state.active_blank_index = 0

def render_fill_blanks(
    level: Optional[Any] = None,
    text_segments: Optional[list[str]] = None,
    keywords: Optional[list[str]] = None,
    options: Optional[list[str]] = None,
    on_finish: Optional[callable] = None,
) -> None:
    ensure_state_initialized()

    if level is not None:
        text_segments = getattr(level, "text_segments", text_segments)
        keywords = getattr(level, "keywords", keywords)
        options = getattr(level, "options", options)

    if not text_segments or not keywords or not options:
        st.warning("Conteúdo do nível não disponível.")
        return

    total_blanks = len(keywords)
    st.caption(f"Progresso: {len(st.session_state.selected_words)}/{total_blanks}")

    built = []
    for i, seg in enumerate(text_segments):
        built.append(seg)
        if i < total_blanks:
            built.append(f" **[{st.session_state.selected_words.get(i, '_____')}]** ")
    st.markdown("".join(built))

    st.write("Lacunas:")
    lac_cols = st.columns(min(6, total_blanks) or 1)
    for i in range(total_blanks):
        with lac_cols[i % len(lac_cols)]:
            active = st.session_state.active_blank_index == i
            label = f"Lacuna {i+1}" + (" ✓" if i in st.session_state.correct_positions else "")
            if st.button(label, key=f"blank_{i}", type=("primary" if active else "secondary")):
                st.session_state.active_blank_index = i
                st.rerun()

    st.subheader("Opções")
    used = set(st.session_state.selected_words.values())
    cols = st.columns(4)
    for idx, opt in enumerate(options):
        with cols[idx % 4]:
            if st.button(opt, key=f"opt_{idx}", disabled=opt in used):
                _place_selected_word(opt, keywords)
                st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Limpar lacuna atual"):
            _clear_current_blank()
            st.rerun()
    with c2:
        if st.button("Limpar tudo"):
            _clear_all()
            st.rerun()

    if all(i in st.session_state.selected_words for i in range(total_blanks)):
        correct_now = sum(
            1
            for i in range(total_blanks)
            if st.session_state.selected_words.get(i, "").lower() == keywords[i].lower()
        )
        st.success(f"Você preencheu {correct_now}/{total_blanks} corretamente.")
        if on_finish:
            on_finish()