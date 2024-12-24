from typing import List, Optional, Dict, Any
import sqlite3


class DatabaseHandler:
    """
    A class to manage interactions with the SQLite database for chatbot history.

    Attributes:
        conn: SQLite connection object.
    """

    def __init__(self, db_path: str = "chatbot_history.db") -> None:
        """
        Initialize the DatabaseHandler with the database path and create the interactions table if it doesn't exist.

        Args:
            db_path (str): Path to the SQLite database file. Defaults to 'chatbot_history.db'.
        """
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self) -> None:
        """
        Create the interactions table in the database if it doesn't already exist.
        """
        query = """
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            feedback TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def log_interaction(
        self, question: str, answer: str, feedback: Optional[str] = None
    ) -> None:
        """
        Log a new interaction into the database.

        Args:
            question (str): The user's question.
            answer (str): The chatbot's answer.
            feedback (Optional[str]): User feedback about the interaction. Defaults to None.
        """
        query = """
        INSERT INTO interactions (question, answer, feedback)
        VALUES (?, ?, ?)
        """
        self.conn.execute(query, (question, answer, feedback))
        self.conn.commit()

    def fetch_all_interactions(self) -> List[sqlite3.Row]:
        """
        Fetch all interactions from the database.

        Returns:
            List[sqlite3.Row]: A list of all rows in the interactions table.
        """
        query = "SELECT * FROM interactions"
        return self.conn.execute(query).fetchall()

    def analyze_feedback(self) -> Dict[str, Any]:
        """
        Analyze user feedback from the interactions table.

        Returns:
            Dict[str, Any]: A dictionary containing statistics on total interactions, positive feedback,
            negative feedback, and error rate.
        """
        interactions = self.fetch_all_interactions()

        total = len(interactions)
        positive = sum(1 for i in interactions if i[4] == "sim")
        negative = sum(1 for i in interactions if i[4] == "não")

        return {
            "total_interactions": total,
            "positive_feedback": positive,
            "negative_feedback": negative,
            "error_rate": negative / total if total > 0 else 0,
        }
