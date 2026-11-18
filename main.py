from urllib.parse import urlparse
from pathlib import Path
from flask import Flask, jsonify, request, current_app
from repository import create_link
import database
import tomllib


def error_response(code, message, status):
    return jsonify({"error": {"code": code, "message": message}}), status


def load_config(path: str = "config.toml") -> dict:
    with open(Path(__file__).resolve().parent / path, "rb") as f:
        raw = tomllib.load(f)
    cfg = {k.upper(): v for k, v in raw.items()}
    cfg["DATABASE_PATH"] = str(
        Path(__file__).resolve().parent / cfg["DATABASE_PATH"]
    )
    return cfg


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(load_config())
    if config:
        app.config.from_mapping(config)
    database.init_app(app)
    register_routes(app)
    return app


def register_routes(app: Flask) -> None:
    @app.errorhandler(404)
    def resource_not_found(error):
        return error_response(
            "not_found", "Ручка или короткий код не найдены", 404
        )

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
        invalid_url = error_response(
            "invalid_url", "Поле `url` отсутствует или не прошло валидацию", 422
        )
        target_url = data.get("url")
        if not isinstance(target_url, str) or not target_url.strip():
            return invalid_url

        target_url = target_url.strip()

        if any(ch.isspace() for ch in target_url):
            return invalid_url
        try:
            parsed = urlparse(target_url)
        except:
            return invalid_url
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
