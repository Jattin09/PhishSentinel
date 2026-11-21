
import sqlite3
from pathlib import Path
from datetime import datetime


# Database location
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "phishsentinel.db"


def initialize_database():
    """Create the scan history table if it does not exist."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            prediction TEXT NOT NULL,
            phishing_probability REAL NOT NULL,
            risk_score INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            scan_time TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_scan(result):
    """Save one URL analysis result."""

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        INSERT INTO scan_history (
            url,
            prediction,
            phishing_probability,
            risk_score,
            risk_level,
            scan_time
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        result["url"],
        result["prediction"],
        result["phishing_probability"],
        result["risk_score"],
        result["risk_level"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_recent_scans(limit=10):
    """Return the most recent scans."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    rows = connection.execute("""
        SELECT *
        FROM scan_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()

    connection.close()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    initialize_database()
    print("PhishSentinel database initialized successfully!")
