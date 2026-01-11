import streamlit as st

st.set_page_config(page_title="Annotator Tracker", layout="centered")

st.title("🧠 Annotator Daily Work Tracker")
st.write("Choose an action:")

if st.button("➕ Upload Daily Work"):
    st.switch_page("uploadDailyWork")

if st.button("📊 Performance Dashboard"):
    st.switch_page("performanceDashboard")

if st.button("🧑‍💻 Annotator Performance Analysis"):
    st.switch_page("annotatorAnalysis")

if st.button("⚖️ All Annotators Comparison"):
    st.switch_page("annotatorsComparison")
