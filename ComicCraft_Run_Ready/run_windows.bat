@echo off
title ComicCraft
if not exist env (
  python -m venv env
)
call env\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Starting ComicCraft...
echo Open http://127.0.0.1:8000
echo.
python -m uvicorn app.main:app --reload
pause
