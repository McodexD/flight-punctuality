import pandas as pd


def prepare(flights):
    df = flights.copy()
    df["delay_minutes"] = pd.to_numeric(df["delay_minutes"])
    df["date_key"] = pd.to_datetime(df["date_key"]).dt.date
    df["is_cancelled"] = df["is_cancelled"] == True
    df["measured"] = df["delay_minutes"].notna() & ~df["is_cancelled"]
    df["delayed"] = (df["is_delayed"] == True) & df["measured"]
    return df


def summarise(df, by):
    grouped = (
        df.groupby(by)
        .agg(
            flights=("flight_key", "size"),
            measured=("measured", "sum"),
            delayed=("delayed", "sum"),
            cancelled_or_removed=("is_cancelled", "sum"),
        )
        .reset_index()
    )
    measured = grouped["measured"].where(grouped["measured"] > 0)
    grouped["delay_rate_pct"] = (grouped["delayed"] / measured * 100).round(1)
    return grouped


def headline(df):
    measured = int(df["measured"].sum())
    delayed = int(df["delayed"].sum())
    return {
        "flights": len(df),
        "measured": measured,
        "delayed": delayed,
        "delay_rate": round(delayed / measured * 100, 1) if measured else 0.0,
        "cancelled": int(df["is_cancelled"].sum()),
    }
