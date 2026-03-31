from support_bot.faq import find_faq_answer
from support_bot.providers import get_llm
from support_bot.logger import get_logger

log = get_logger(__name__)

SYSTEM_PROMPT = """You are a helpful customer support assistant.
Answer questions clearly and concisely. If you don't know something,
say so and suggest the customer contact support@example.com."""


def get_response(message: str, history: list[dict]) -> dict:
    faq_answer = find_faq_answer(message)
    if faq_answer:
        return {"answer": faq_answer, "source": "faq"}

    llm = get_llm()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for h in history[-6:]:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": message})

    response = llm.invoke(messages)
    return {"answer": response.content, "source": "ai"}