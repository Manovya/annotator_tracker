import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(layout="wide")
st.title("📊 Performance Dashboard")

conn = get_connection()
df = pd.read_sql("SELECT * FROM work_logs", conn)
conn.close()

df["date"] = pd.to_datetime(df["date"])

c1, c2, c3 = st.columns(3)
c1.metric("Annotators", df["annotator"].nunique())
c2.metric("Total Annotations", int(df["annotations_completed"].sum()))
c3.metric("Projects", df["project"].nunique())

daily = (
    df[df["status"] != "Leave"]
    .groupby("date")["annotations_completed"]
    .sum()
)

st.line_chart(daily)
