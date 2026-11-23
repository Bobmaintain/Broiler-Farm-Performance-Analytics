import pandas as pd

from src.metrics import add_performance_metrics, validate_records


def sample_frame():
    return pd.DataFrame([
        {
            "date": "2026-01-01", "flock_id": "TEST-01",
            "birds_placed": 1000, "live_birds": 995, "feed_kg": 80,
            "avg_weight_kg": 0.20, "mortality_count": 5,
            "feed_cost_kwd": 20, "other_cost_kwd": 5,
        },
        {
            "date": "2026-01-02", "flock_id": "TEST-01",
            "birds_placed": 1000, "live_birds": 990, "feed_kg": 100,
            "avg_weight_kg": 0.25, "mortality_count": 5,
            "feed_cost_kwd": 25, "other_cost_kwd": 3,
        },
    ])


def test_valid_records_pass():
    assert validate_records(sample_frame()) == []


def test_negative_feed_is_rejected():
    frame = sample_frame()
    frame.loc[0, "feed_kg"] = -1
    assert any("feed_kg" in error for error in validate_records(frame))


def test_cumulative_metrics():
    result = add_performance_metrics(sample_frame(), initial_chick_weight_kg=0.04)
    assert result["cumulative_mortality"].tolist() == [5, 10]
    assert result["cumulative_feed_kg"].tolist() == [80, 180]
    assert result["cumulative_total_cost_kwd"].tolist() == [25, 53]
    assert result["fcr"].iloc[-1] > 0
