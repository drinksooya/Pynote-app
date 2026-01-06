import streamlit as st
from src.pynote.main.main import add, DB_FILE  # We are importing the 'add' command from your file

st.set_page_config(page_title="PyNote Web", page_icon="📓")

st.title("📓 PyNote Web")
st.write("This is the Web Home for your Typer application.")

# Web input fields
title = st.text_input("Note Title")
content = st.text_area("Note Content")

if st.button("Add Note"):
    if title and content:
        # We call the 'add' function directly from your main.py
        try:
            add(title, content)
            st.success(f"Success! Note '{title}' added to {DB_FILE if 'DB_FILE' in locals() else 'the database'}.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter both a title and content.")