from openai import OpenAI

# Pointing to your free local Ollama server engine instead of the cloud
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required field by the package, but ignored by Ollama
)


def generate_response(prompt: str):
    response = client.chat.completions.create(
        model="llama3.2:3b",  # Using your newly downloaded free local 3B model
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI research assistant. "
                    "Answer questions using the provided context only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    # Correct list index extraction syntax
    return response.choices[0].message.content
