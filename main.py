import sqlite3
from datetime import UTC, datetime
from urllib.parse import urlparse

from flask import Flask, jsonify, request

import database
from codes import generate_code
import tomllib
from pathlib import Path


def load_config(path: str = "config.toml") -> dict:
    with open(Path(__file__).resolve().parent / path, "rb") as f:
        return tomllib.load(f)


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


<<<<<<< HEAD
@app.post("/api/links")
def create_shortlinks():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response(
            "invalid_json", "Тело запроса не является корректным JSON", 400
        )
=======
def register_routes(app: Flask) -> None:
    @app.errorhandler(404)
    def resource_not_found(error):
        return error_response(
            "not_found", "Ручка или короткий код не найдены", 404
        )

    @app.get("/")
    def index():
        return app.send_static_file("index.html")
>>>>>>> a83b955 (fix: minors)

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
    for _ in range(5):
        code = generate_code()
        try:
            db.execute(
                "INSERT INTO links (code, created_at, target_url) VALUES (?, ?, ?)",
                (code, datetime.now(UTC).isoformat(), target_url),
            )
<<<<<<< HEAD
            db.commit()
            return code
        except sqlite3.IntegrityError:
            db.rollback()
            raise RuntimeError("Не удалось сгенерировать уникальный код")

    return jsonify(
        {
            "code": code,
            "short_url": f"{load_config().BASE_URL}/{code}",
            "target_url": target_url,
        }
    ), 201
=======
        invalid_url = error_response(
            "invalid_url", "Поле `url` отсутствует или не прошло валидацию", 422
        )
        target_url = data.get("url")
        if not isinstance(target_url, str) or not target_url.strip():
            return invalid_url
        target_url = target_url.strip()

        parsed = urlparse(target_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            return invalid_url

        code = create_link(target_url)

        return jsonify(
            {
                "code": code,
                "short_url": f"{current_app.config["BASE_URL"]}/{code}",
                "target_url": target_url,
            }
        ), 201
>>>>>>> a83b955 (fix: minors)
