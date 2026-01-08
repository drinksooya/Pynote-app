import os
from typer.testing import CliRunner
from pynote.main.main import app, DB_FILE

runner = CliRunner()

def test_add_note_flow():
    # 1. SETUP
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    # 2. ACTION: Call the app directly with the arguments
    # Do NOT include "add" here
    result = runner.invoke(app, ["Test Title", "Test Content"])

    # 3. ASSERT
    assert result.exit_code == 0
    assert "Success" in result.stdout
    assert os.path.exists(DB_FILE)

    # 4. CLEANUP
    # if os.path.exists(DB_FILE):
    #     os.remove(DB_FILE)