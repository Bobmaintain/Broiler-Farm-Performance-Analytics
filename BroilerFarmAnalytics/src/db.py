import sqlite3
from pathlib import Path

import pandas as pd

TABLE_NAME = "daily_flock_records"


def initialize_database(db_path: str | Path) -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                date TEXT NOT NULL,
                flock_id TEXT NOT NULL,
                birds_placed INTEGER NOT NULL,
                live_birds INTEGER NOT NULL,
                feed_kg REAL NOT NULL,
                avg_weight_kg REAL NOT NULL,
                mortality_count INTEGER NOT NULL,
                feed_cost_kwd REAL NOT NULL,
                other_cost_kwd REAL NOT NULL,
                PRIMARY KEY (date, flock_id)
            )
        """)
        conn.commit()


def replace_records(df: pd.DataFrame, db_path: str | Path) -> None:
    """Replace the demo database contents with the supplied validated records."""
    initialize_database(db_path)
    clean = df.copy()
    clean["date"] = pd.to_datetime(clean["date"]).dt.strftime("%Y-%m-%d")
    columns = [
        "date", "flock_id", "birds_placed", "live_birds", "feed_kg",
        "avg_weight_kg", "mortality_count", "feed_cost_kwd", "other_cost_kwd",
    ]
    with sqlite3.connect(db_path) as conn:
        conn.execute(f"DELETE FROM {TABLE_NAME}")
        clean[columns].to_sql(TABLE_NAME, conn, if_exists="append", index=False)
        conn.commit()


def list_flocks(db_path: str | Path) -> list[str]:
    initialize_database(db_path)
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            f"SELECT DISTINCT flock_id FROM {TABLE_NAME} ORDER BY flock_id"
        ).fetchall()
    return [row[0] for row in rows]


def fetch_flock_records(flock_id: str, db_path: str | Path) -> pd.DataFrame:
    initialize_database(db_path)
    query = f"""
        SELECT date, flock_id, birds_placed, live_birds, feed_kg,
               avg_weight_kg, mortality_count, feed_cost_kwd, other_cost_kwd
        FROM {TABLE_NAME}
        WHERE flock_id = ?
        ORDER BY date
    """
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn, params=(flock_id,))
