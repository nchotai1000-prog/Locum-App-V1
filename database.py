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


def add_shift(shift_date, hours, hourly_rate):
    connection = get_connection()
    connection.execute(
        "INSERT INTO shifts (shift_date, hours, hourly_rate) VALUES (?, ?, ?)",
        (shift_date, hours, hourly_rate),
    )
    connection.commit()
    connection.close()


def add_shift(shift_date, hours, hourly_rate):
    connection = get_connection()
    connection.execute(
        "INSERT INTO shifts (shift_date, hours, hourly_rate) VALUES (?, ?, ?)",
        (shift_date, hours, hourly_rate),
    )
    connection.commit()
    connection.close()


def get_shifts():
    connection = get_connection()
    shifts = connection.execute(
        "SELECT * FROM shifts ORDER BY shift_date DESC, id DESC"
    ).fetchall()
    connection.close()
    return shifts
