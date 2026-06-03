def build_history_context(messages):
    history = ""

    for msg in messages:
        history += (
            f"{msg.role}: "
            f"{msg.content}\n"
        )

    return history
