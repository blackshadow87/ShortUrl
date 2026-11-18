# justfile
set windows-shell := ["powershell.exe", "-c"]

# Таска для запуска сервера
run:
<<<<<<< HEAD
    uvicorn main:app --interface wsgi
=======
    uv run uvicorn "main:create_app" --factory --reload --interface wsgi
>>>>>>> a83b955 (fix: minors)
