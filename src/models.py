from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI


def get_embeddings(
    model_name: str = "sentence-transformers/all-mpnet-base-v2",
) -> HuggingFaceEmbeddings:
    """
    Initialize and return a HuggingFaceEmbeddings object.

    Args:
        model_name (str): The name of the embedding model to use. Defaults to 'sentence-transformers/all-mpnet-base-v2'.

    Returns:
        HuggingFaceEmbeddings: An instance of the HuggingFaceEmbeddings class.
    """
    return HuggingFaceEmbeddings(model_name=model_name)


def get_llm(model: str = "gemini-1.5-flash") -> ChatGoogleGenerativeAI:
    """
    Initialize and return a ChatGoogleGenerativeAI model instance.

    Args:
        model (str): The name of the language model to use. Defaults to 'gemini-1.5-flash'.

    Returns:
        ChatGoogleGenerativeAI: An instance of the ChatGoogleGenerativeAI class.
    """
    return ChatGoogleGenerativeAI(model=model)
