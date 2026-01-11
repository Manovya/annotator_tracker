import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(layout="wide")
st.title("🧑‍💻 Annotator Performance Analysis")

conn = get_connection()
df = pd.read_sql("SELECT * FROM work_logs", conn)
conn.close()

df["date"] = pd.to_datetime(df["date"])
df.fillna("Unknown", inplace=True)

annotator = st.selectbox(
    "Select Annotator",
    sorted(df["annotator"].unique())
)

person_df = df[df["annotator"] == annotator]

st.metric(
    "Total Annotations",
    int(person_df["annotations_completed"].sum())
)

task_perf = person_df.groupby("task")["annotations_completed"].sum()
st.bar_chart(task_perf)

daily = person_df.groupby("date")["annotations_completed"].sum()
st.line_chart(daily)
