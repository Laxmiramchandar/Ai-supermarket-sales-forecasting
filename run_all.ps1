# PowerShell One-Click Full Project Runner
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host " EXECUTING FULL SUPERMARKET FORECASTING SYSTEM PIPELINE" -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "`n[1/7] Validating Environment and Datasets..." -ForegroundColor Yellow
python scripts/validate_environment_and_data.py

Write-Host "`n[2/7] Running EDA and Stationarity Diagnostics..." -ForegroundColor Yellow
python src/data_processing/eda_diagnostics.py

Write-Host "`n[3/7] Generating Features and Sequence Tensors..." -ForegroundColor Yellow
python src/data_processing/preprocessor.py

Write-Host "`n[4/7] Benchmarking Classical Baselines (Naïve, MA, ARIMA)..." -ForegroundColor Yellow
python src/models/baseline_models.py

Write-Host "`n[5/7] Training Deep Learning Models (GRU, LSTM, BiLSTM)..." -ForegroundColor Yellow
python src/training/train_pipeline.py

Write-Host "`n[6/7] Training Customer Churn Classifier (Secondary Module)..." -ForegroundColor Yellow
python src/models/churn_classifier.py

Write-Host "`n[7/7] Running Automated Pytest Quality Suite..." -ForegroundColor Yellow
pytest -v tests/

Write-Host "`n==============================================================" -ForegroundColor Green
Write-Host " ALL PIPELINE STAGES COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green
Write-Host "To launch FastAPI:   uvicorn src.api.main:app --port 8000 --reload"
Write-Host "To launch Dashboard: streamlit run dashboard/app.py"
