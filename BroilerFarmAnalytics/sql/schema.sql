CREATE TABLE IF NOT EXISTS daily_flock_records (
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
);
