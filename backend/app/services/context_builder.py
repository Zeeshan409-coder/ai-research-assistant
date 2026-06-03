def build_context(
    results,
    max_chars=8000
):

    context = ""
    used = []

    for result in results:

        text = result["text"]

        if len(context) + len(text) > max_chars:
            break

        context += text + "\n\n"

        used.append(result)

    return context, used
