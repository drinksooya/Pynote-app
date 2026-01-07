import streamlit as st
import json
import os
from src.pynote.main.main import add

st.set_page_config(page_title="PyNote Web", page_icon="📓", layout="wide")

# --- USER ACCESS ---
st.sidebar.title("🔐 Access Control")
# Using type="password" hides the key as you type it
user_key = st.sidebar.text_input("Enter Secret Key", type="password")

# --- SIDEBAR: VIEW NOTES ---
st.sidebar.title("🗂️ Your Private Notes")
DB_FILE = "notes_db.json"

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        all_notes = json.load(f)

    if user_key:
        # LOGIC CHANGE: Filter notes to only show those matching the user_key
        # We check if the note has a 'key' field and if it matches
        my_notes = [n for n in all_notes if n.get('key') == user_key]

        if my_notes:
            for note in reversed(my_notes):
                with st.sidebar.expander(f"📌 {note['title']}"):
                    st.write(note['content'])
                    st.caption(f"ID: {note['id']}")
        else:
            st.sidebar.info("No notes found for this key.")
    else:
        st.sidebar.warning("Please enter your key to see your notes.")
else:
    st.sidebar.info("Database file not found.")

# --- MAIN AREA: ADD NOTES ---
st.title("📓 PyNote Web")
st.write("Add a new note to your private collection.")

with st.container():
    title = st.text_input("Note Title")
    content = st.text_area("Note Content", height=150)

    if st.button("Add Note", use_container_width=True):
        if not user_key:
            st.error("You must enter a Secret Key in the sidebar before adding a note!")
        elif title and content:
            try:
                # LOGIC CHANGE: We pass the user_key to your add function
                # Note: You may need to update your main.py add() function
                # to accept and save this third 'key' argument.
                add(title, content, user_key)
                st.success(f"Added '{title}' to your private vault!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Both fields are required.")