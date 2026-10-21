import streamlit as st

from db import load_flights
from metrics import headline, prepare, summarise

st.set_page_config(page_title="Flight punctuality", layout="wide")


def sidebar_filters(df):
    st.sidebar.header("Filters")
    dates = sorted(df["date_key"].unique())
    airports = sorted(df["airport_name"].unique())
    selected_dates = st.sidebar.multiselect("Dates", dates, default=dates)
    selected_directions = st.sidebar.multiselect(
        "Direction", ["arrival", "departure"], default=["arrival", "departure"]
    )
    selected_airports = st.sidebar.multiselect("Airports", airports, default=airports)
    min_measured = st.sidebar.slider("Minimum measured flights per airline", 1, 100, 20)
    return selected_dates, selected_directions, selected_airports, min_measured


def apply_filters(df, dates, directions, airports):
    return df[
        df["date_key"].isin(dates)
        & df["direction"].isin(directions)
        & df["airport_name"].isin(airports)
    ]


def show_headline(df):
    numbers = headline(df)
    columns = st.columns(4)
    columns[0].metric("Flights", f"{numbers['flights']:,}")
    columns[1].metric("Delayed (more than 15 min)", f"{numbers['delayed']:,}")
    columns[2].metric("Delay rate", f"{numbers['delay_rate']} %")
    columns[3].metric("Cancelled or removed", f"{numbers['cancelled']:,}")


def show_by_date(df):
    st.subheader("Delayed flights by date")
    data = summarise(df, ["date_key", "direction"])
    data["date_key"] = data["date_key"].astype(str)
    left, right = st.columns(2)
    left.caption("Number of delayed flights")
    left.bar_chart(data, x="date_key", y="delayed", color="direction", stack=False)
    right.caption("Delay rate (% of flights with a known time)")
    right.bar_chart(data, x="date_key", y="delay_rate_pct", color="direction", stack=False)


def show_by_airport(df):
    st.subheader("Delays by airport")
    data = summarise(df, "airport_name")
    left, right = st.columns(2)
    left.caption("Number of delayed flights")
    left.bar_chart(data, x="airport_name", y="delayed")
    right.caption("Delay rate (%)")
    right.bar_chart(data, x="airport_name", y="delay_rate_pct")


def show_by_airline(df, min_measured):
    st.subheader("Delays by airline")
    data = summarise(df, "airline_name")
    data = data[data["measured"] >= min_measured].sort_values("delay_rate_pct", ascending=False)
    if data.empty:
        st.info("No airline has enough measured flights for the current filters.")
        return
    left, right = st.columns(2)
    left.caption("Delay rate (%) for the 15 airlines with the highest rate")
    left.bar_chart(data.head(15), x="airline_name", y="delay_rate_pct")
    right.caption("Airline details")
    right.dataframe(data, hide_index=True, use_container_width=True)


def main():
    st.title("Flight punctuality at Swedish airports")
    st.caption(
        "A flight counts as delayed when it is more than 15 minutes later than scheduled. "
        "Delay rates only include flights with an estimated or actual time. "
        "Cancelled and removed flights are counted separately and left out of the delay numbers."
    )
    df = prepare(load_flights())
    dates, directions, airports, min_measured = sidebar_filters(df)
    filtered = apply_filters(df, dates, directions, airports)
    if filtered.empty:
        st.warning("No flights match the current filters.")
        return
    show_headline(filtered)
    show_by_date(filtered)
    show_by_airport(filtered)
    show_by_airline(filtered, min_measured)


main()
