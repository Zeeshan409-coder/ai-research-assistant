from qdrant_client import QdrantClient

# Adjusted to localhost since our backend is running natively on Windows
client = QdrantClient(
    host="localhost",
    port=6333
)
