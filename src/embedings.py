from dotenv import dotenv_values
# do pracy z qdrantem
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
# do pracy z openai
from openai import OpenAI

from src.books import lem_books

env = dotenv_values(".env")

EMBEDDING_DIM = 1536

EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_client():
    return OpenAI(api_key=env["OPENAI_API_KEY"])


def get_embedding(text):
    openai_client = get_openai_client()
    result = openai_client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL,
        dimensions=EMBEDDING_DIM,
    )

    return result.data[0].embedding


def get_qdrant_client(memory=True):
    url = ":memory:" if memory else "qdrant.db"
    client = QdrantClient(url)
    return client


QDRANT_COLLECTION_NAME = "lem_books"


def init_collection(client, books):
    """
    Tworzy kolekcję i wstawia książki, jeśli kolekcja nie istnieje
    """
    if not client.collection_exists(collection_name=QDRANT_COLLECTION_NAME):
        # print("Tworzę kolekcję")
        client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )

        points = [
            PointStruct(
                id=idx,
                vector=get_embedding(f'{book["name"]} {book.get("genere","")}'),
                payload=book
            )
            for idx, book in enumerate(books)
        ]

        client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=points
        )


def search_books(client, query, top_k=1):
    """
    Szuka w kolekcji Qdrant po embeddingu query
    Zwraca listę payloadów (książki)
    """
    q_emb = get_embedding(query)
    results = client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=q_emb,
        limit=top_k
    )
    # zwracamy listę tuple: (payload, score)
    return [(r.payload,
            r.score)
            for r in results]


def print_top_result(results):
    """
    Prosty helper do pokazania wyniku w konsoli
    """
    if results:
        top = results[0]
        print('TYTUŁ:', top["name"])
        print('KSIĄŻKA:', top["book"])
        print('OPIS FABUŁY:', top.get('description', 'brak'))
        print('GENRE:', top.get("genere", "brak"))