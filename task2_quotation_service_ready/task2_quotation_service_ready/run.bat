@echo off
echo Starting Quotation Service...
echo.
echo API Documentation will be available at:
echo   - Swagger UI: http://127.0.0.1:8000/docs
echo   - ReDoc:      http://127.0.0.1:8000/redoc
echo   - Health:     http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo.
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
