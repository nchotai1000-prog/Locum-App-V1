import sqlite3

DATABASE = "locum.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shift_date TEXT NOT NULL,
            hours REAL NOT NULL,
            hourly_rate REAL NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()