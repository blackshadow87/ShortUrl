from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DATABASE_PATH = str(PROJECT_ROOT / "shorturl.db")
BASE_URL = "http://localhost:8000"
CODE_LENGTH = 7