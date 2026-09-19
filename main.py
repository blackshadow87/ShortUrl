import sqlite3
from datetime import UTC, datetime
from urllib.parse import urlparse

from flask import Flask, jsonify, redirect, request

import config
import database
from codes import encode_id

app = Flask(__name__)
database.init_app(app)


def error_response(code, message, status):
    return jsonify({"error": {"code": code, "message": message}}), status


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.post("/api/links")
def create_shortlinks():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response(
            "invalid_json", "Тело запроса не является корректным JSON", 400
        )

    target_url = data.get("url")
    if not isinstance(target_url, str) or not target_url.strip():
        return error_response(
            "invalid_url", "Поле `url` отсутствует или не прошло валидацию", 422
        )

    parsed = urlparse(target_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return error_response(
            "invalid_url", "Поле `url` отсутствует или не прошло валидацию", 422
        )

    db = database.get_db()
    try:
        cursor = db.execute(
            "INSERT INTO links (code, created_at, target_url) VALUES (?, ?, ?)",
            ("", datetime.now(UTC).isoformat(), target_url),
        )
        row_id = cursor.lastrowid
        code = encode_id(row_id)
        db.execute("UPDATE links SET code = ? WHERE id = ?", (code, row_id))
        db.commit()
    except sqlite3.Error:
        db.rollback()
        return error_response("internal_error", "Внутренняя ошибка сервиса", 500)

    return jsonify(
        {
            "code": code,
            "short_url": f"{config.BASE_URL}/{code}",
            "target_url": target_url,
        }
    ), 201


