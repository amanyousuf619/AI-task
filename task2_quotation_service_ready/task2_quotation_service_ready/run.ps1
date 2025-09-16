Write-Host "Starting Quotation Service..." -ForegroundColor Green
Write-Host ""
Write-Host "API Documentation will be available at:" -ForegroundColor Yellow
Write-Host "  - Swagger UI: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host "  - ReDoc:      http://127.0.0.1:8000/redoc" -ForegroundColor Cyan
Write-Host "  - Health:     http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host ""

& .venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
