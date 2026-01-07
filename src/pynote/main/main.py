import json
import os
import logging  # Import the logging module
from typing import List
from pydantic import BaseModel
import typer

# Configure logging: This tells Python how to format the logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = typer.Typer()
DB_FILE = "notes_db.json"

class Note(BaseModel):
    id: int
    title: str
    content: str

def load_notes() -> List[dict]:
    if not os.path.exists(DB_FILE):
        logging.warning(f"{DB_FILE} not found. Starting with an empty list.") # Log a warning
        return []
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load notes: {e}") # Log a critical error
        return []

def save_notes(notes: List[dict]):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(notes, f, indent=4)
        logging.info("Successfully saved notes to database.") # Log a success message
    except Exception as e:
        logging.error(f"Could not save note! Error: {e}") # Log an error if saving fails


@app.command()
def add(title: str, content: str, key: str = "default"):
    logging.info(f"Attempting to add note: {title} with key privacy")  # Log the start of an action
    notes = load_notes()
    new_id = len(notes) + 1

    # We add the key to the note data so it can be filtered later
    new_note = Note(id=new_id, title=title, content=content)
    note_data = new_note.model_dump()
    note_data["key"] = key  # Assign the secret key to the note

    notes.append(note_data)
    save_notes(notes)
    typer.echo(f"Success! Note #{new_id} added to your private vault.")


if __name__ == "__main__":
    logging.info("App started")  # Track when the app is initialized
    app()