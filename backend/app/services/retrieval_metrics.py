def calculate_context_stats(results):

    total_chars = sum(
        len(r["text"])
        for r in results
    )

    return {
        "chunks": len(results),
        "characters": total_chars
    }
