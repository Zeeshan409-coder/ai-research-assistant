import json
import httpx

# Corrected host to localhost so your local Python code can connect to Ollama flawlessly
OLLAMA_URL = "http://localhost:11434/api/generate"


async def stream_response(prompt: str, model: str = "llama3.2:3b"):
    """
    Asynchronous generator that communicates with Ollama's REST endpoint,
    streaming model response chunks over the local loopback interface.
    """
    # Using infinite timeout thresholds to prevent standard HTTP socket dropouts during heavy inferences
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True  # 👈 Crucial parameter: enables newline-delimited token streaming chunks
            }
        ) as response:
            
            # Efficiently read from the active transport wire line-by-line
            async for line in response.aiter_lines():
                if not line:
                    continue

                try:
                    data = json.loads(line)
                    # Extract the individual generated token character fragment safely
                    token = data.get("response", "")
                    
                    if token:
                        yield token
                        
                except Exception:
                    continue
