import os
import sqlite3

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locum.db")


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


def get_month_total(month):
    connection = get_connection()
    row = connection.execute(
        "SELECT SUM(hours * hourly_rate) AS total FROM shifts WHERE shift_date LIKE ?",
        (month + "-%",),
    ).fetchone()
    connection.close()
    return row["total"] or 0


def delete_shift(shift_id):
    connection = get_connection()
    connection.execute("DELETE FROM shifts WHERE id = ?", (shift_id,))
    connection.commit()
    connection.close()
