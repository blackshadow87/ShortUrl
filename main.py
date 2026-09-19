from flask import Flask, jsonify, request
from datetime import timezone, datetime
from urllib.parse import urlparse
import database, config
import string, secrets, sqlite3


app = Flask(__name__)
database.init_app(app)

@app.get("/")
def index():
    return app.send_static_file("index.html")

@app.get("/health")
def health_check():
    return jsonify({"status" : "ok"}), 200

def generate_random_code(length):
    ALPHABET = string.ascii_letters + string.digits
    return "".join(secrets.choice(ALPHABET) for _ in range(length))

@app.post("/api/links")
def create_shortlinks():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            "error": {
            "code": "invalid_json",
            "message": "Тело запроса не является корректным JSON"}}), 400
    
    target_url = data.get('url')
    if not isinstance(target_url, str) or not target_url.strip():
        return jsonify({
            "error": 
            {"code": "invalid_url",
            "message": "Поле `url` отсутствует или не прошло валидацию"}}), 422

    parsed = urlparse(target_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return jsonify({
    "error": {
    "code": "invalid_url",
    "message": "Поле `url` отсутствует или не прошло валидацию"
    }}), 422

    db = database.get_db()
    cursor = db.cursor()

    for attempt in range(5):  
        code = generate_random_code(config.CODE_LENGTH)
        try:      
            short_url = f"{config.BASE_URL}/{code}"
            cursor.execute(
            "INSERT INTO links (code, created_at, target_url) VALUES (?, ?, ?)", 
            (code, datetime.now(timezone.utc).isoformat(), target_url))
            db.commit()
            break
        except sqlite3.IntegrityError:
            db.rollback()
            if attempt == 4:
                return jsonify({
                    "error": {
                    "code": "internal_error",
                    "message": "Внутренняя ошибка сервиса"
                    }}),500
    return jsonify({"code": code, "short_url": short_url,
                    "target_url": target_url}), 201