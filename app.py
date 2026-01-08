import streamlit as st
from supabase import create_client, Client

# 1. SETUP SUPABASE CONNECTION
# Paste your actual URL and Key between the quotes below
url: str = "https://xmafxwjwizaomwglooaa.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhtYWZ4d2p3aXphb213Z2xvb2FhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc3ODIzOTMsImV4cCI6MjA4MzM1ODM5M30.NrRfLuZc2qPIhnP6tPUqIpGov9M9xfX31ql7U1efwYs"
supabase: Client = create_client(url, key)

st.set_page_config(page_title="PyNote Web", page_icon="📓", layout="wide")


# --- GATEKEEPER LOGIC ---
def password_entered():
    """Checks whether the app password is correct."""
    if st.session_state["password_input"] == "Loveminghao":
        st.session_state["password_correct"] = True
        del st.session_state["password_input"]
    else:
        st.session_state["password_correct"] = False


def check_password():
    """Returns True if the user is authenticated."""
    if st.session_state.get("password_correct", False):
        return True

    st.title("🔒 PyNote is Locked")
    st.text_input("Enter App Password", type="password", on_change=password_entered, key="password_input")

    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Password incorrect")
    return False


# Halt the app here if not logged in
if not check_password():
    st.stop()

# --- SIDEBAR: VIEW NOTES FROM SUPABASE ---
st.sidebar.title("🗂️ Cloud Notes")

try:
    # This pulls notes from your Supabase table in real-time
    response = supabase.table("notes").select("*").order("created_at", desc=True).execute()
    all_notes = response.data

    if all_notes:
        for note in all_notes:
            with st.sidebar.expander(f"📌 {note['title']}"):
                st.write(note['content'])
                st.caption(f"Saved at: {note['created_at']}")
    else:
        st.sidebar.info("Your cloud vault is empty.")
except Exception as e:
    st.sidebar.error(f"Cloud Connection Error: {e}")

# --- MAIN AREA: ADD NOTES TO SUPABASE ---
st.title("📓 PyNote Web")
st.write("Add a note to your permanent cloud storage.")

with st.container():
    title = st.text_input("Note Title")
    content = st.text_area("Note Content", height=150)

    if st.button("Add Note", use_container_width=True):
        if title and content:
            try:
                # This logic replaces your old 'add()' function from main.py
                data = {"title": title, "content": content}
                supabase.table("notes").insert(data).execute()

                st.success(f"Successfully saved '{title}' to the cloud!")
                st.rerun()
            except Exception as e:
                st.error(f"Error saving to cloud: {e}")
        else:
            st.warning("Both fields are required.")