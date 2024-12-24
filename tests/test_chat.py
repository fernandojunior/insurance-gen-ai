import pytest
from unittest.mock import Mock, patch
from chat import Chat, QA, setup_retriever, setup_chain

@pytest.fixture
def mock_chat_components():
    """Fixture to provide mocked components for testing Chat."""
    mock_embeddings = Mock()
    mock_llm = Mock()
    mock_retriever = Mock()
    mock_chain = Mock()
    mock_db_handler = Mock()
    mock_qa_chain = Mock()
    mock_qa_chain.run.return_value = "Mocked answer"
    
    with patch("your_module_name.models.get_embeddings", return_value=mock_embeddings), \
         patch("your_module_name.models.get_llm", return_value=mock_llm), \
         patch("your_module_name.setup_retriever", return_value=mock_retriever), \
         patch("your_module_name.setup_chain", return_value=mock_qa_chain), \
         patch("your_module_name.db.DatabaseHandler", return_value=mock_db_handler):
        yield {
            "mock_retriever": mock_retriever,
            "mock_qa_chain": mock_qa_chain,
            "mock_db_handler": mock_db_handler,
        }

def test_chat_ask_and_log(mock_chat_components):
    """Test the ask and log functionalities of the Chat class."""
    chat_template = "You are an assistant. {context}{question}{chat_history}"
    index_folder_path = "/mock/index/path"
    chat = Chat(index_folder_path, chat_template)

    # Test `ask` method
    question = "What is the capital of France?"
    qa = chat.ask(question)

    assert isinstance(qa, QA), "The returned object should be an instance of QA."
    assert qa.question == question, "The QA object should store the correct question."
    assert qa.answer == "Mocked answer", "The QA object should store the mocked answer."

    # Test `set_feedback`
    feedback = "Helpful answer"
    chat.set_feedback(qa, feedback)
    assert qa.feedback == feedback, "The QA object should store the provided feedback."

    # Test `log` method
    logged_qa = chat.log(qa)
    mock_db_handler = mock_chat_components["mock_db_handler"]
    mock_db_handler.log_interaction.assert_called_once_with(
        qa.question, qa.answer, qa.feedback
    )
    assert logged_qa is qa, "The `log` method should return the same QA object."

def test_chat_get_history(mock_chat_components):
    """Test the get_history method of the Chat class."""
    mock_db_handler = mock_chat_components["mock_db_handler"]
    mock_db_handler.fetch_all_interactions.return_value = [
        {"question": "Q1", "answer": "A1", "feedback": "Good"},
        {"question": "Q2", "answer": "A2", "feedback": "Average"},
    ]
    chat_template = "You are an assistant. {context}{question}{chat_history}"
    index_folder_path = "/mock/index/path"
    chat = Chat(index_folder_path, chat_template)

    history = chat.get_history()
    assert len(history) == 2, "The history should contain 2 interactions."
    assert history[0]["question"] == "Q1", "The first history item should match the mock data."
    assert history[1]["feedback"] == "Average", "The second feedback should match the mock data."
