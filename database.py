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
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            day_rate REAL NOT NULL,
            ooh_rate REAL NOT NULL,
            ooh_start TEXT NOT NULL,
            ooh_end TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()


def add_shift(shift_date, start_time, end_time, day_rate, ooh_rate, ooh_start, ooh_end):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO shifts
            (shift_date, start_time, end_time, day_rate, ooh_rate, ooh_start, ooh_end)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (shift_date, start_time, end_time, day_rate, ooh_rate, ooh_start, ooh_end),
    )
    connection.commit()
    connection.close()


def get_shifts():
    connection = get_connection()
    shifts = connection.execute(
        "SELECT * FROM shifts ORDER BY shift_date DESC, start_time DESC, id DESC"
    ).fetchall()
    connection.close()
    return shifts


def get_shifts_for_month(month):
    connection = get_connection()
    shifts = connection.execute(
        "SELECT * FROM shifts WHERE shift_date LIKE ?",
        (month + "-%",),
    ).fetchall()
    connection.close()
    return shifts


def delete_shift(shift_id):
    connection = get_connection()
    connection.execute("DELETE FROM shifts WHERE id = ?", (shift_id,))
    connection.commit()
    connection.close()
