# from qdrant_client import QdrantClient
# from qdrant_client.models import PointStruct, VectorParams, Distance

# EMBEDDING_DIM = 1536

# EMBEDDING_MODEL = "text-embedding-3-small"
# QDRANT_COLLECTION_NAME = "lem_books"


# def get_qdrant_client(memory=True):
#     url = ":memory:" if memory else "qdrant.db"
#     client = QdrantClient(url)
#     return client


# def init_collection(client, books):
#     """
#     Tworzy kolekcję i wstawia książki, jeśli kolekcja nie istnieje
#     """
#     if not client.collection_exists(collection_name=QDRANT_COLLECTION_NAME):
#         # print("Tworzę kolekcję")
#         client.create_collection(
#             collection_name=QDRANT_COLLECTION_NAME,
#             vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
#         )

#         points = [
#             PointStruct(
#                 id=idx,
#                 vector=get_embedding(f'{book["name"]} {book.get("genere","")}'),
#                 payload=book
#             )
#             for idx, book in enumerate(books)
#         ]

#         client.upsert(
#             collection_name=QDRANT_COLLECTION_NAME,
#             points=points
#         )


# def search_books(client, query, top_k=1):
#     """
#     Szuka w kolekcji Qdrant po embeddingu query
#     Zwraca listę payloadów (książki)
#     """
#     q_emb = get_embedding(query)
#     results = client.search(
#         collection_name=QDRANT_COLLECTION_NAME,
#         query_vector=q_emb,
#         limit=top_k
#     )
#     # zwracamy listę tuple: (payload, score)
#     return [(r.payload,
#             r.score)
#             for r in results]


# def print_top_result(results):
#     """
#     Prosty helper do pokazania wyniku w konsoli
#     """
#     if results:
#         top = results[0]
#         print('TYTUŁ:', top["name"])
#         print('KSIĄŻKA:', top["book"])
#         print('OPIS FABUŁY:', top.get('description', 'brak'))
#         print('GENRE:', top.get("genere", "brak"))


from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

from src.embeddings import get_embedding, EMBEDDING_DIM
from src.books import lem_books

QDRANT_COLLECTION_NAME = "lem_books"


def get_qdrant_client(memory: bool = True):
    '''
    Creates a Qdrant client for working with embedding collections.

Args:
    memory (bool): If True, the database runs in RAM (non-persistent).
                   If False, the database is persistent on disk ('qdrant.db').

Returns:
    QdrantClient: A client object for managing vector collections and performing searches.
    '''
    url = ":memory:" if memory else "qdrant.db"
    return QdrantClient(url)


def init_collection(client: QdrantClient):
    '''
    Initializes a Qdrant collection if it does not already exist.

    - Uses the provided Qdrant client (in this case, in-memory RAM database).
    - Checks whether the collection exists.
    - If not, creates the collection named 'lem_books'.

    VectorParams define the properties of the vectors in this collection:
        - size = EMBEDDING_DIM → length of each embedding (e.g., 1536)
        - distance = Distance.COSINE → method for measuring vector similarity (cosine similarity)
    '''

    if not client.collection_exists(QDRANT_COLLECTION_NAME):
        client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE
            ),
        )



def index_books(client: QdrantClient):
    '''
    Indexes books into the Qdrant collection by converting them into embeddings
    and storing them in the vector database.

    Args:
        client (QdrantClient): Qdrant client instance used to communicate with the database.

    Process:
        - Creates a list of points (PointStruct) representing books in vector space.
        - Each point consists of:
            id -> unique identifier of the point (index in the list),
            vector -> embedding of the text ("name + genre"),
            payload -> full book data (metadata used for displaying search results).
        - If a point with the given id already exists → it is updated.
        - If it does not exist → it is inserted as a new record.
    '''
    points = [
        PointStruct(
            id=i,
            vector=get_embedding(f"{b['name']} {b['genere']}"),
            payload=b
        )
        for i, b in enumerate(lem_books)
    ]

    client.upsert(
        collection_name=QDRANT_COLLECTION_NAME,
        points=points
    )



def search_books(client: QdrantClient, query: str, top_k: int = 3):
    vector = get_embedding(query)

    '''
    Searches for the most similar books in the Qdrant collection using vector similarity.

Args:
    client (QdrantClient): Qdrant client instance used to communicate with the database.
    query (str): User query describing the topic of interest.
    top_k (int, optional): Number of top matching results to return. Defaults to 3.

Returns:
    list: List of search results sorted by similarity score (descending).
          Each result contains:
            - payload: stored book metadata,
            - score: similarity score between query and stored vectors.

Process:
    - Converts the input query text into an embedding vector using OpenAI.
    - Performs a vector similarity search in the Qdrant collection.
    - Returns the top_k most similar vectors along with their metadata and scores.
    '''

    results = client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=vector,
        limit=top_k
    )

    return results