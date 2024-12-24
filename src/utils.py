import os
import uuid
from typing import List


def get_unique_id() -> str:
    """
    Generate a unique identifier.

    Returns:
        str: A unique UUID4 string.
    """
    return str(uuid.uuid4())


def list_files_by_datetime(folder_path: str) -> List[str]:
    """
    List files in a directory, ordered by modification date.

    Args:
        folder_path (str): Path to the directory.

    Returns:
        List[str]: A list of filenames ordered by modification date (oldest to newest).
    """
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    # Sort files by modification timestamp
    sorted_files = sorted(
        files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f))
    )

    return sorted_files


def list_pdfs(folder_path: str) -> List[str]:
    """
    List all PDF files in a directory.

    Args:
        folder_path (str): Path to the directory.

    Returns:
        List[str]: A list of file paths for all PDF files in the directory.
    """
    return [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.endswith(".pdf")
    ]
