from typing import List, Optional, Dict, Any
import sqlite3


class DatabaseHandler:
    """
    A class to manage interactions with the SQLite database for chatbot history.

    Attributes:
        conn: SQLite connection object.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initialize the DatabaseHandler with the database path and create the interactions table if it doesn't exist.

        Args:
            db_path (str): Path to the SQLite database file. Defaults to 'chatbot_history.db'.
        """
        self.db_path = db_path
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
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(query)
        self.conn.commit()
        self.conn.close()

    def log_interaction(self, question: str, answer: str) -> None:
        """
        Log a new interaction into the database.

        Args:
            question (str): The user's question.
            answer (str): The chatbot's answer.
        """
        query = """
        INSERT INTO interactions (question, answer)
        VALUES (?, ?)
        """
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute(query, (question, answer))
        self.conn.commit()
        self.conn.close()

    def fetch_all_interactions(self) -> List[sqlite3.Row]:
        """
        Fetch all interactions from the database.

        Returns:
            List[sqlite3.Row]: A list of all rows in the interactions table.
        """
        query = "SELECT * FROM interactions ORDER BY timestamp"
        self.conn = sqlite3.connect(self.db_path)
        result = self.conn.execute(query).fetchall()
        self.conn.close()

        return result
