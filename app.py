import streamlit as st
from supabase import create_client, Client
import logging
import threading
import time

# --- 1. MONITORING: HEALTH CHECK HEARTBEAT ---
# Setup logging to output to your server terminal
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def run_health_check():
    """A background function that logs 'I'm okay!' every 60 seconds."""
    while True:
        logging.info("HEALTH CHECK: I'm okay! (Heartbeat)")
        time.sleep(60)


# Start the heartbeat thread only once
if "health_check_started" not in st.session_state:
    thread = threading.Thread(target=run_health_check, daemon=True)
    thread.start()
    st.session_state["health_check_started"] = True

# --- 2. SETUP SUPABASE CONNECTION ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="PyNote Web", page_icon="📓", layout="wide")


# --- GATEKEEPER LOGIC ---
def password_entered():
    if st.session_state["password_input"] == "Loveminghao":
        st.session_state["password_correct"] = True
        del st.session_state["password_input"]
    else:
        st.session_state["password_correct"] = False


def check_password():
    if st.session_state.get("password_correct", False):
        return True
    st.title("🔒 PyNote is Locked")
    st.text_input("Enter App Password", type="password", on_change=password_entered, key="password_input")
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()

# --- SIDEBAR: VIEW NOTES FROM SUPABASE ---
st.sidebar.title("🗂️ Cloud Notes")

try:
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
    # MONITORING: Log the error to the server console
    logging.error(f"HEALTH CHECK: Cloud Connection Error - {e}")
    st.sidebar.error(f"Cloud Connection Error: {e}")

# --- MAIN AREA: ADD NOTES TO SUPABASE ---
st.title("📓 PyNote Web")
st.write("Add a note to your permanent cloud storage.")

with st.container():
    title = st.text_input("Note Title")
    content = st.text_area("Note Content", height=150)

    if st.button("Add Note", use_container_width=True):
        if title and content:
            # Fix the yellow squiggly line with 'as _'
            with st.spinner("Uploading to cloud...") as _:
                try:
                    data = {"title": title, "content": content}
                    supabase.table("notes").insert(data).execute()

                    # MONITORING: Log a success event
                    logging.info(f"HEALTH CHECK: Successfully added note '{title}'")

                    st.success(f"Successfully saved '{title}' to the cloud!")
                    st.rerun()
                except Exception as e:
                    # MONITORING: Log the failure event
                    logging.error(f"HEALTH CHECK: Failed to add note - {e}")
                    st.error(f"Error saving to cloud: {e}")