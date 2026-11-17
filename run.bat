@echo off
title Currency Converter & Affordability Analyzer
echo =========================================================
echo Starting Affordability Analyzer Web Application...
echo Local URL: http://127.0.0.1:8000
echo =========================================================
cd /d "%~dp0"
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
pause

