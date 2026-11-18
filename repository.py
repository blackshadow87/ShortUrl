import sqlite3
import database
from codes import generate_code
from datetime import UTC, datetime
from flask import current_app


def create_link(target_url: str) -> str:
    for _ in range(5):
        try:
            db = database.get_db()
            length = current_app.config["CODE_LENGTH"]
            code = generate_code(length)
            db.execute(
                "INSERT INTO links (code, created_at, target_url) VALUES (?, ?, ?)",
                (code, datetime.now(UTC).isoformat(), target_url),
            )
            db.commit()
            return code
        except sqlite3.IntegrityError:
            db.rollback()
            raise RuntimeError("Не удалось сгенерировать уникальный код")
