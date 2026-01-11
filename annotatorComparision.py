import streamlit as st
import pandas as pd
from database import get_connection

st.set_page_config(layout="wide")
st.title("⚖️ All Annotators Comparison")

conn = get_connection()
df = pd.read_sql("SELECT * FROM work_logs", conn)
conn.close()

total = (
    df.groupby("annotator")["annotations_completed"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(total)

task_wise = (
    df.groupby(["annotator", "task"])["annotations_completed"]
    .sum()
    .unstack()
    .fillna(0)
)

st.dataframe(task_wise)
