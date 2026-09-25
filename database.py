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
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL DEFAULT '',
            day_rate REAL NOT NULL,
            ooh_rate REAL NOT NULL,
            ooh_start TEXT NOT NULL,
            ooh_end TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shift_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            specialty TEXT NOT NULL DEFAULT '',
            day_rate REAL NOT NULL,
            ooh_rate REAL NOT NULL,
            ooh_start TEXT NOT NULL,
            ooh_end TEXT NOT NULL,
            profile_id INTEGER REFERENCES profiles(id)
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS goals (
            month TEXT PRIMARY KEY,
            target REAL NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()


def add_profile(name, specialty, day_rate, ooh_rate, ooh_start, ooh_end):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO profiles
            (name, specialty, day_rate, ooh_rate, ooh_start, ooh_end)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, specialty, day_rate, ooh_rate, ooh_start, ooh_end),
    )
    connection.commit()
    connection.close()


def get_profiles():
    connection = get_connection()
    profiles = connection.execute(
        "SELECT * FROM profiles ORDER BY name"
    ).fetchall()
    connection.close()
    return profiles


def delete_profile(profile_id):
    connection = get_connection()
    connection.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
    connection.commit()
    connection.close()


def add_shift(
    shift_date,
    start_time,
    end_time,
    specialty,
    day_rate,
    ooh_rate,
    ooh_start,
    ooh_end,
    profile_id,
):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO shifts
            (shift_date, start_time, end_time, specialty, day_rate, ooh_rate,
             ooh_start, ooh_end, profile_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            shift_date,
            start_time,
            end_time,
            specialty,
            day_rate,
            ooh_rate,
            ooh_start,
            ooh_end,
            profile_id,
        ),
    )
    connection.commit()
    connection.close()


def get_shifts():
    connection = get_connection()
    shifts = connection.execute(
        """
        SELECT shifts.*, profiles.name AS profile_name
        FROM shifts
        LEFT JOIN profiles ON shifts.profile_id = profiles.id
        ORDER BY shifts.shift_date DESC, shifts.start_time DESC, shifts.id DESC
        """
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


def set_goal(month, target):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO goals (month, target) VALUES (?, ?)
        ON CONFLICT(month) DO UPDATE SET target = excluded.target
        """,
        (month, target),
    )
    connection.commit()
    connection.close()


def get_goal(month):
    connection = get_connection()
    row = connection.execute(
        "SELECT target FROM goals WHERE month = ?", (month,)
    ).fetchone()
    connection.close()
    return row["target"] if row else None
