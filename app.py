import streamlit as st
import json
import os
from src.pynote.main.main import add  # Your existing logic

st.set_page_config(page_title="PyNote Web", page_icon="📓", layout="wide")

# --- SIDEBAR: VIEW NOTES ---
st.sidebar.title("🗂️ Saved Notes")
DB_FILE = "notes_db.json"

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        notes = json.load(f)

    if notes:
        for note in reversed(notes):  # Show newest first
            with st.sidebar.expander(f"📌 {note['title']}"):
                st.write(note['content'])
                st.caption(f"ID: {note['id']}")
    else:
        st.sidebar.info("No notes saved yet.")
else:
    st.sidebar.info("Database file not found.")

# --- MAIN AREA: ADD NOTES ---
st.title("📓 PyNote Web")
st.write("Add a new note to your collection.")

with st.container():
    title = st.text_input("Note Title")
    content = st.text_area("Note Content", height=150)

    if st.button("Add Note", use_container_width=True):
        if title and content:
            try:
                add(title, content)
                st.success(f"Added '{title}'!")
                st.rerun()  # This refreshes the app so the new note shows up in the sidebar
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Both fields are required.")