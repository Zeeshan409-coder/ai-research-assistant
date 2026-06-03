from app.services.context_builder import build_context
from app.services.chat_history_builder import build_history_context  # 👈 Integrated history builder


def build_prompt(query: str, search_results, history=None, max_chars=8000):

    # 1. Compress raw document context blocks cleanly below the character ceiling
    context_text, used_results = build_context(
        results=search_results,
        max_chars=max_chars
    )

    # 2. Compile recent chat database rows into a readable dialog block
    history_text = ""
    if history:
        history_text = build_history_context(history)

    # 3. Construct the comprehensive context package for your stateless LLM
    prompt = f"""
You are an expert research assistant. Use the following document context and recent conversation history to answer the question.

Document Context:
{context_text}

Recent Conversation History:
{history_text}

Current User Question:
{query}

Answer:
"""

    return prompt, used_results
