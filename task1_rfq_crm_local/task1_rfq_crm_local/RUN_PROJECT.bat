@echo off
echo ===============================================================================
echo                    RFQ CRM PROJECT - AUTOMATIC RUNNER
echo ===============================================================================
echo.

echo Activating virtual environment...
call .venv\Scripts\activate

echo.
echo Running RFQ Pipeline...
python src/run_pipeline.py

echo.
echo ===============================================================================
echo Pipeline completed! Check the data folder for output files.
echo ===============================================================================
echo.
echo Output files created:
echo - data/rfq_log.csv (spreadsheet data)
echo - data/crm_opportunities.jsonl (CRM data)  
echo - data/outbox/reply_*.txt (auto-reply emails)
echo - data/alerts.log (system messages)
echo.

pause
