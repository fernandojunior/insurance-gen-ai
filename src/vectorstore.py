from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.base import Embeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

import config
import models
import utils


def load_documents(folder_path: str) -> List[dict]:
    """
    Load and process all PDF documents from the specified folder.

    Args:
        folder_path (str): Path to the folder containing PDF files.

    Returns:
        List[dict]: A list of document objects, each containing content and metadata.
    """
    pdf_files = utils.list_pdfs(folder_path)
    documents = []

    for pdf_file in pdf_files:
        loader = PyPDFLoader(pdf_file)
        documents.extend(loader.load_and_split())

    return documents


def split_text(
    documents: List[dict], chunk_size: int = 1000, chunk_overlap: int = 200
) -> List[dict]:
    """
    Split text into smaller chunks for efficient embedding and retrieval.

    Args:
        documents (List[dict]): List of document objects to be split.
        chunk_size (int): Maximum size of each chunk. Defaults to 1000.
        chunk_overlap (int): Overlap size between consecutive chunks. Defaults to 200.

    Returns:
        List[dict]: A list of split document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)


def create_vector_store(
    documents: List[dict], embeddings: Embeddings, folder_path
) -> str:
    """
    Create a vector store index from documents and save it locally.

    Args:
        documents (List[dict]): List of document chunks to index.
        embeddings (Embeddings): Embedding model to use for vectorization.

    Returns:
        str: The unique identifier of the saved vector store.
    """
    request_id = utils.get_unique_id()

    vectorstore = FAISS.from_documents(documents, embeddings)
    file_name = f"{request_id}.bin"
    vectorstore.save_local(index_name=file_name, folder_path=folder_path)

    return request_id


def run(input_folder_path, output_folder_path) -> None:
    """
    Main function to load documents, process text, and create a vector store index.
    """
    files = utils.list_files_by_datetime(config.output_folder_path)
    files = [f for f in files if f.endswith(".faiss")]

    if len(files) > 0:
        return files[0].split(".")[0]

    documents = load_documents(input_folder_path)
    chunks = split_text(documents)
    embeddings = models.get_embeddings()
    vector_id = create_vector_store(chunks, embeddings, output_folder_path)
    print(f"Vector store ID: {vector_id}")

    return vector_id
