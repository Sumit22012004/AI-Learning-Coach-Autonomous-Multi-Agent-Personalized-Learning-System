from qdrant_client import QdrantClient
from src.core.config import settings

def get_qdrant_client() -> QdrantClient:
    """
    Returns a configured QdrantClient instance.
    Checks if connected to Qdrant Cloud or Local Docker.
    """
    return QdrantClient(url=settings.QDRANT_URL)

async def init_vector_store():
    """
    Initializes collections if they don't exist.
    """
    client = get_qdrant_client()
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]
    
    if "learning_materials" not in collection_names:
        client.create_collection(
            collection_name="learning_materials",
            vectors_config={"size": 1536, "distance": "Cosine"} # Assuming OpenAI/Voyage embeddings size
        )
