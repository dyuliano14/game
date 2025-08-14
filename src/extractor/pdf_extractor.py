import re
import random
from typing import List, Dict, Any

try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None  # type: ignore


def extract_pdf_text(pdf_path: str) -> str:
    """Extrai o texto bruto do PDF."""
    if PdfReader is None:
        raise RuntimeError("PyPDF2 não disponível. Instale PyPDF2.")
    reader = PdfReader(pdf_path)
    text_parts = []
    for page in reader.pages:
        try:
            text_parts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(text_parts)


def split_into_articles(text: str) -> List[Dict[str, Any]]:
    """
    Divide o texto em artigos pelo padrão 'Art. N'.
    Retorna [{id, title, text}].
    """
    norm = re.sub(r"[ \t]+", " ", text)
    parts = re.split(r"(?=(?:\bArt\.\s*\d+))", norm, flags=re.IGNORECASE)
    articles = []
    for part in parts:
        clean = part.strip()
        if not clean:
            continue
        m = re.match(r"(Art\.\s*\d+)", clean, flags=re.IGNORECASE)
        title = m.group(1) if m else "Introdução"
        articles.append({
            "id": len(articles),
            "title": title,
            "text": clean,
        })
    return articles


def _pick_candidate_words(text: str) -> List[str]:
    # Palavras candidatas: 5+ letras, não tudo maiúsculo, sem números
    words = re.findall(r"\b[^\W\d_]{5,}\b", text, flags=re.UNICODE)
    words = [w for w in words if not w.isupper()]
    uniq = []
    seen = set()
    for w in words:
        lw = w.lower()
        if lw not in seen:
            seen.add(lw)
            uniq.append(w)
    return uniq


def generate_fill_blanks_from_article(article_text: str, max_blanks: int = 5, seed: int | None = None) -> Dict[str, Any]:
    """
    Gera dados para o jogo de lacunas a partir do texto do artigo.
    Retorna {text_segments, keywords, options}.
    Estratégia:
      - escolhe até 5 ocorrências espalhadas ao longo do texto (estratificado por posição)
      - opções incluem as 5 corretas + distratores retirados do próprio texto
      - usa semente (seed) para gerar sempre o mesmo conjunto por PDF/artigo
    """
    rng = random.Random(seed)
    text = article_text

    def iter_candidates(regex_pat: str):
        for m in re.finditer(regex_pat, text, flags=re.UNICODE):
            w = m.group(0)
            if not w.isupper():
                yield (m.start(), m.end(), w)

    occ = list(iter_candidates(r"\b[^\W\d_]{5,}\b"))
    if not occ:
        occ = list(iter_candidates(r"\b[^\W\d_]{3,}\b"))

    if not occ:
        return {"text_segments": [text], "keywords": [], "options": []}

    occ.sort(key=lambda t: t[0])
    total_len = len(text)

    desired = min(max_blanks, len(occ))
    chosen = []
    used_words_lower = set()

    for k in range(desired):
        start_band = int(k * (total_len / desired))
        end_band = int((k + 1) * (total_len / desired))
        band = [o for o in occ if start_band <= o[0] < end_band and o[2].lower() not in used_words_lower]
        pick = None
        if band:
            pick = rng.choice(band)
        else:
            remaining = [o for o in occ if o[2].lower() not in used_words_lower]
            if remaining:
                pick = rng.choice(remaining)
        if pick:
            chosen.append(pick)
            used_words_lower.add(pick[2].lower())

    if not chosen:
        return {"text_segments": [text], "keywords": [], "options": []}

    chosen.sort(key=lambda t: t[0])

    segments: List[str] = []
    blanks: List[str] = []
    cursor = 0
    for (start, end, w) in chosen:
        segments.append(text[cursor:start])
        blanks.append(text[start:end])
        cursor = end
    segments.append(text[cursor:])

    chosen_set = {b.lower() for b in blanks}
    pool_words = [w for (_, _, w) in occ if w.lower() not in chosen_set]
    seen = set()
    pool_unique = []
    for w in pool_words:
        lw = w.lower()
        if lw not in seen:
            seen.add(lw)
            pool_unique.append(w)

    distractor_count = min(5, max(0, len(pool_unique)))
    distractors = rng.sample(pool_unique, distractor_count) if pool_unique else []

    options = blanks[:] + distractors
    rng.shuffle(options)

    return {
        "text_segments": segments,
        "keywords": blanks,
        "options": options,
    }