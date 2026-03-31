import json
from pathlib import Path
from difflib import SequenceMatcher
from support_bot import settings
from support_bot.logger import get_logger

log = get_logger(__name__)


def _load_faq() -> list[dict]:
    path = Path(settings.faq_path)
    if not path.exists():
        log.warning(f"FAQ file not found: {path}")
        return []
    return json.loads(path.read_text(encoding="utf-8"))


FAQ = _load_faq()


def find_faq_answer(query: str) -> str | None:
    best_score = 0.0
    best_answer = None

    for item in FAQ:
        score = SequenceMatcher(
            None, query.lower(), item["question"].lower()
        ).ratio()
        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    if best_score >= settings.similarity_threshold:
        log.info(f"FAQ match found (score={best_score:.2f})")
        return best_answer

    log.info(f"No FAQ match (best score={best_score:.2f}) — falling back to AI")
    return None