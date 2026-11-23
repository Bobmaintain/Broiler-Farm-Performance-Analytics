import pandas as pd

REQUIRED_COLUMNS = [
    "date", "flock_id", "birds_placed", "live_birds", "feed_kg",
    "avg_weight_kg", "mortality_count", "feed_cost_kwd", "other_cost_kwd",
]

NUMERIC_COLUMNS = [
    "birds_placed", "live_birds", "feed_kg", "avg_weight_kg",
    "mortality_count", "feed_cost_kwd", "other_cost_kwd",
]


def validate_records(df: pd.DataFrame) -> list[str]:
    """Return data-quality errors. An empty list means basic checks passed."""
    errors = []
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        return [f"Missing required columns: {', '.join(missing)}"]

    if df.empty:
        return ["The CSV contains no records."]

    parsed_dates = pd.to_datetime(df["date"], errors="coerce")
    if parsed_dates.isna().any():
        errors.append("Every date must be a valid date.")

    for col in NUMERIC_COLUMNS:
        values = pd.to_numeric(df[col], errors="coerce")
        if values.isna().any():
            errors.append(f"{col} must contain numeric values.")
        elif (values < 0).any():
            errors.append(f"{col} cannot contain negative values.")

    if not errors:
        if (pd.to_numeric(df["live_birds"]) > pd.to_numeric(df["birds_placed"])).any():
            errors.append("Live birds cannot exceed birds placed.")
        if (pd.to_numeric(df["mortality_count"]) > pd.to_numeric(df["birds_placed"])).any():
            errors.append("Daily mortality cannot exceed birds placed.")
        if (pd.to_numeric(df["avg_weight_kg"]) <= 0).any():
            errors.append("Average weight must be greater than zero.")
        if df.duplicated(["date", "flock_id"]).any():
            errors.append("There must not be duplicate date/flock_id records.")

    return errors


def add_performance_metrics(
    df: pd.DataFrame, initial_chick_weight_kg: float = 0.04
) -> pd.DataFrame:
    """Calculate flock-level cumulative indicators from daily snapshots."""
    result = df.copy()
    result["date"] = pd.to_datetime(result["date"])
    result = result.sort_values("date").reset_index(drop=True)

    result["cumulative_mortality"] = result["mortality_count"].cumsum()
    result["cumulative_feed_kg"] = result["feed_kg"].cumsum()
    result["cumulative_feed_cost_kwd"] = result["feed_cost_kwd"].cumsum()
    result["cumulative_other_cost_kwd"] = result["other_cost_kwd"].cumsum()
    result["cumulative_total_cost_kwd"] = (
        result["cumulative_feed_cost_kwd"] + result["cumulative_other_cost_kwd"]
    )

    starting_biomass = result["birds_placed"].iloc[0] * initial_chick_weight_kg
    current_biomass = result["live_birds"] * result["avg_weight_kg"]
    result["estimated_liveweight_gain_kg"] = current_biomass - starting_biomass

    gain = result["estimated_liveweight_gain_kg"].where(
        result["estimated_liveweight_gain_kg"] > 0
    )
    result["fcr"] = result["cumulative_feed_kg"] / gain

    placed = result["birds_placed"].iloc[0]
    result["cumulative_mortality_rate_pct"] = (
        result["cumulative_mortality"] / placed * 100 if placed else 0
    )
    return result
