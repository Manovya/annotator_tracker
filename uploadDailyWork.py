import streamlit as st
import pandas as pd
from database import get_connection, create_table

create_table()

st.set_page_config(layout="wide")
st.title("➕ Upload Daily Work")

PROJECTS = [
    "Nephroplus", "Adult RD", "Netra", "ICU Automation",
    "V Sitter", "Airways", "VRASS", "CPOT", "Respiratory Distress"
]

TASKS = [
    "Classification", "BBOX", "Keypoints", "Ground Truth",
    "Segmentation", "Database", "Data Collection", "Leave"
]

# -------- FORM --------
with st.form("daily_entry"):
    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date")
        annotator = st.text_input("Annotator Name")
        project = st.selectbox("Project", PROJECTS)

    with col2:
        task = st.selectbox("Task", TASKS)
        status = st.selectbox("Status", ["In Progress", "Done", "Leave"])
        annotations = st.number_input("Annotations Completed", min_value=0)

    comments = st.text_area("Comments")
    submit = st.form_submit_button("✅ Submit")

if submit:
    conn = get_connection()
    conn.execute("""
        INSERT INTO work_logs
        (date, annotator, project, task, status, annotations_completed, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        str(date), annotator, project, task,
        status, annotations, comments
    ))
    conn.commit()
    conn.close()
    st.success("✅ Work uploaded successfully")

# -------- EXCEL IMPORT --------
st.divider()
st.header("🔄 Import OLD Excel Data (One Time)")

uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)

    if st.button("📥 Import"):
        conn = get_connection()
        for _, row in df.iterrows():
            if pd.isna(row.get("Column 1")):
                continue

            date = str(row.get("Column 1"))
            annotator = row.get("Annotator", "")
            project = row.get("Projects", "")
            comments = row.get("Comments", "")

            for i in ["", " 2"]:
                task = row.get(f"Task{i}")
                status = row.get(f"Status{i}")
                count = row.get(f"No of Annotations Completed{i}")

                if pd.notna(task):
                    conn.execute("""
                        INSERT INTO work_logs
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        date, annotator, project,
                        task, status, int(count or 0), comments
                    ))

        conn.commit()
        conn.close()
        st.success("✅ Excel data imported")
