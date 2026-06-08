import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import timedelta

st.set_page_config(
    page_title="My Period Tracker",
    page_icon="🌸",
    layout="wide"
)

# ==========================
# Create Files
# ==========================

FILES = {
    "periods.csv": [
        "start_date",
        "end_date"
    ],

    "daily_logs.csv": [
        "date",
        "weight",
        "exercise_minutes",
        "breast_tenderness",
        "bloating",
        "mood",
        "stress"
    ]
}

for file, columns in FILES.items():

    if not os.path.exists(file):

        pd.DataFrame(
            columns=columns
        ).to_csv(
            file,
            index=False
        )

# ==========================
# Load Data
# ==========================

period_df = pd.read_csv(
    "periods.csv"
)

daily_df = pd.read_csv(
    "daily_logs.csv"
)

# ==========================
# Title
# ==========================

st.title("🌸 Myat's Personal Period Tracker")

tabs = st.tabs(
    [
        "Dashboard",
        "Periods",
        "Daily Tracking"
    ]
)

# ==========================
# DASHBOARD
# ==========================

with tabs[0]:

    st.header("Cycle Statistics")

    if len(period_df) >= 2:

        dates = pd.to_datetime(
            period_df["start_date"]
        ).sort_values()

        cycle_lengths = (
            dates.diff()
            .dt.days
            .dropna()
        )

        avg_cycle = round(
            cycle_lengths.mean(),
            1
        )

        shortest = int(
            cycle_lengths.min()
        )

        longest = int(
            cycle_lengths.max()
        )

        median_cycle = int(
            cycle_lengths.median()
        )

        last_period = dates.iloc[-1]

        earliest = (
            last_period +
            timedelta(days=shortest)
        )

        likely = (
            last_period +
            timedelta(days=median_cycle)
        )

        latest = (
            last_period +
            timedelta(days=longest)
        )

        c1,c2,c3,c4 = st.columns(4)

        c1.metric(
            "Average",
            f"{avg_cycle} days"
        )

        c2.metric(
            "Median",
            median_cycle
        )

        c3.metric(
            "Shortest",
            shortest
        )

        c4.metric(
            "Longest",
            longest
        )

        st.subheader(
            "🔮 Next Period Prediction"
        )

        st.info(
            f"""
Earliest: {earliest.date()}

Most Likely: {likely.date()}

Latest: {latest.date()}
"""
        )

        chart_df = pd.DataFrame({
            "Cycle Length":
            cycle_lengths.values
        })

        fig = px.line(
            chart_df,
            y="Cycle Length",
            markers=True,
            title="Cycle Length Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "Please enter at least 2 periods."
        )

# ==========================
# PERIOD TAB
# ==========================

with tabs[1]:

    st.header("Add Period")

    start_date = st.date_input(
        "Start Date"
    )

    end_date = st.date_input(
        "End Date"
    )

    if st.button(
        "Save Period"
    ):

        new_row = pd.DataFrame(
            {
                "start_date":[start_date],
                "end_date":[end_date]
            }
        )

        period_df = pd.concat(
            [period_df,new_row],
            ignore_index=True
        )

        period_df.to_csv(
            "periods.csv",
            index=False
        )

        st.success(
            "Period saved."
        )

    st.subheader(
        "Period History"
    )

    st.dataframe(
        period_df,
        use_container_width=True
    )

# ==========================
# DAILY TAB
# ==========================

with tabs[2]:

    st.header(
        "Daily Tracking"
    )

    date = st.date_input(
        "Date",
        key="daily"
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=20.0,
        max_value=200.0,
        value=57.0,
        step=0.1
    )

    exercise = st.number_input(
        "Exercise Minutes",
        min_value=0,
        value=0
    )

    breast = st.checkbox(
        "Breast Tenderness"
    )

    bloating = st.checkbox(
        "Bloating"
    )

    mood = st.slider(
        "Mood",
        1,
        5,
        3
    )

    stress = st.slider(
        "Stress",
        1,
        5,
        3
    )

    if st.button(
        "Save Daily Log"
    ):

        new_row = pd.DataFrame(
            {
                "date":[date],
                "weight":[weight],
                "exercise_minutes":[exercise],
                "breast_tenderness":[
                    int(breast)
                ],
                "bloating":[
                    int(bloating)
                ],
                "mood":[mood],
                "stress":[stress]
            }
        )

        daily_df = pd.concat(
            [daily_df,new_row],
            ignore_index=True
        )

        daily_df.to_csv(
            "daily_logs.csv",
            index=False
        )

        st.success(
            "Daily log saved."
        )

    st.subheader(
        "Daily History"
    )

    st.dataframe(
        daily_df,
        use_container_width=True
    )

    if len(daily_df) > 0:

        daily_df["date"] = pd.to_datetime(
            daily_df["date"]
        )

        fig = px.line(
            daily_df,
            x="date",
            y="weight",
            title="Weight Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        exercise_chart = (
            daily_df
            .groupby("date")
            ["exercise_minutes"]
            .sum()
            .reset_index()
        )

        fig2 = px.bar(
            exercise_chart,
            x="date",
            y="exercise_minutes",
            title="Exercise Minutes"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )