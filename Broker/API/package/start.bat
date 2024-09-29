@echo off
REM Install dependencies
pip install -r requirements.txt
REM Run FASTAPI application
uvicorn app:app --host 0.0.0.0 --port 8010
pause