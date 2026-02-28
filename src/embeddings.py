from dotenv import dotenv_values
from openai import OpenAI

env = dotenv_values(".env")

EMBEDDING_DIM = 1536
EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_client():
    return OpenAI(api_key=env["OPENAI_API_KEY"])


def get_embedding(text: str) -> list[float]:
    """
    Creates an embedding of a text using the OpenAI model.

    Args:
        text (str): The text for which the embedding will be generated.

    Returns:
        list[float]: A vector of floating-point numbers representing the semantic 
                     meaning of the text (length = EMBEDDING_DIM).

    Note:
        This function handles only a **single text**. 
        If you want batch embeddings, you need to use a list of texts and a loop 
        or a separate function.
    """

    client = get_openai_client()
    result = client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL,
        dimensions=EMBEDDING_DIM,
    )
    return result.data[0].embedding