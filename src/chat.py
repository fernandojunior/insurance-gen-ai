from typing import Any, Dict, List, Optional, Union

from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.base import Embeddings
from langchain.schema import BaseRetriever
from langchain.llms.base import BaseLLM

import utils
import database as db
import models


def setup_retriever(
    store_folder_path: str,
    embeddings: Embeddings,
    search_type: str = "similarity",
    search_kwargs: Optional[Dict[str, Union[str, int]]] = None,
) -> BaseRetriever:
    """
    Set up the retriever using FAISS and embeddings.

    Args:
        store_folder_path (str): Path to the folder containing the FAISS index files.
        embeddings (Embeddings): Embedding model instance.
        search_type (str): The type of search to perform. Defaults to 'similarity'.
        search_kwargs (Optional[Dict[str, Union[str, int]]]): Additional search parameters. Defaults to {"k": 5}.

    Returns:
        BaseRetriever: Configured retriever object.
    """
    search_kwargs = search_kwargs or {"k": 5}
    files = utils.list_files_by_datetime(store_folder_path)

    if not files:
        raise Exception("store_folder_path empty" + ",".join(files))

    files = [f for f in files if f.endswith(".faiss")]

    if not files:
        raise Exception("*.faiss file not found" + ",".join(files))

    index_name = [f.split(".faiss")[0] for f in files][0]

    vectorstore = FAISS.load_local(
        index_name=index_name,
        folder_path=store_folder_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )

    return vectorstore.as_retriever(
        search_type=search_type, search_kwargs=search_kwargs
    )


def setup_chain(
    retriever: BaseRetriever,
    llm: BaseLLM,
    chat_template: str,
) -> ConversationalRetrievalChain:
    """
    Set up a conversational retrieval chain with memory.

    Args:
        retriever (BaseRetriever): The retriever object.
        llm (BaseLLM): The language model instance.
        chat_template (str): Template string for the conversational prompt.

    Returns:
        ConversationalRetrievalChain: Configured conversational retrieval chain.
    """
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="question",
        output_key="answer",
        return_messages=True,
    )

    prompt_template = PromptTemplate(
        template=chat_template,
        input_variables=["context", "question", "chat_history"],
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt_template},
    )


class QA:
    """
    Class to represent a question and answer pair.
    """

    def __init__(self, question: str, answer: Optional[str] = None) -> None:
        """
        Initialize a QA instance.

        Args:
            question (str): The user's question.
            answer (Optional[str]): The model's answer. Defaults to None.
        """
        self.question = question
        self.answer = answer

    def set_answer(self, answer: str) -> None:
        """
        Set the answer for the question.

        Args:
            answer (str): The model's answer.
        """
        self.answer = answer

    def __repr__(self) -> str:
        """
        String representation of the QA object.

        Returns:
            str: A string representing the QA instance.
        """
        return f"QA(question='{self.question}', answer='{self.answer}')"


class Chat:
    """
    Chat system class to handle user interactions, retrieval, and logging.
    """

    def __init__(self, store_folder_path: str, db_path: str, chat_template: str) -> None:
        """
        Initialize the Chat instance.

        Args:
            store_folder_path (str): Path to the folder containing FAISS index files.
            db_path (str): Path to the folder containing database data.
            chat_template (str): Template string for the chat prompts.
        """
        embeddings = models.get_embeddings()
        llm = models.get_llm()
        retriever = setup_retriever(
            store_folder_path=store_folder_path, embeddings=embeddings
        )
        self._qa_chain = setup_chain(retriever, llm, chat_template)
        self._db_handler = db.DatabaseHandler(db_path=db_path)

    def ask(self, question: str) -> QA:
        """
        Process a user's question through the QA chain.

        Args:
            question (str): The user's question.

        Returns:
            QA: A QA object with the question and model's answer.
        """
        qa = QA(question=question)
        qa.set_answer(self._qa_chain.run({"question": question}))
        return qa

    def log(self, qa: QA) -> QA:
        """
        Log the interaction in the database.

        Args:
            qa (QA): The QA instance to log.

        Returns:
            QA: The logged QA instance.
        """
        self._db_handler.log_interaction(qa.question, qa.answer)
        return qa

    def get_history(self) -> List[db.sqlite3.Row]:
        """
        Retrieve the chat history from the database.

        Returns:
            List[sqlite3.Row]: A list of rows representing the interaction history.
        """
        return self._db_handler.fetch_all_interactions()
