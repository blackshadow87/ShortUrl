# justfile
set windows-shell := ["powershell.exe", "-c"]

# Таска для запуска сервера
run:
    uv run uvicorn "main:create_app" --factory --reload --interface wsgi
