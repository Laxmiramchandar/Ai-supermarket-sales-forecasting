# 🛒 AI-Powered Supermarket Sales Forecasting & Analytics System

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Deep%20Learning-TensorFlow%20%7C%20PyTorch-orange.svg)](https://tensorflow.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production%20Ready-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)](https://streamlit.io)
[![Tests](https://img.shields.io/badge/Pytest-12%20Passed%20%28100%25%29-brightgreen.svg)](https://docs.pytest.org)
[![Docker](https://img.shields.io/badge/Docker-Multi--Container-2496ED.svg)](https://www.docker.com/)

An enterprise-grade, end-to-end Time Series Forecasting and Analytics System leveraging Deep Learning (GRU, LSTM, Bidirectional LSTM) benchmarked against classical statistical models (ARIMA, Moving Average, Naïve). Includes production FastAPI microservices, an interactive Streamlit analytics dashboard, automated testing, containerization, data drift monitoring, and cloud deployment blueprints.

---

## 🏛️ System Architecture

```
[Raw Data] -> [Schema Validation] -> [Stationarity Tests (ADF/KPSS)] -> [Lag/Rolling Features]
                                                                                │
┌───────────────────────────────────────────────────────────────────────────────┘
▼
[Chronological Split] -> [Baseline Benchmarks (Naïve, MA, ARIMA)]
         │
         ▼
[Deep Learning Models (LSTM, GRU, BiLSTM)] -> [Evaluation (RMSE, MAE, MAPE, WAPE)]
         │
         ▼
[Model Serialization & Artifact Storage]
         │
         ├────────────────────────────────────────┬─────────────────────────────┐
         ▼                                        ▼                             ▼
[FastAPI Microservice]                   [Streamlit Dashboard]        [Evidently Drift Monitor]
  • /health, /info, /predict               • What-If Scenarios          • KS & PSI Drift Tests
  • Pydantic V2 Validation                 • Interactive Plotly         • Automated Alerts
         │                                        │                             │
         └────────────────────────────────────────┴─────────────────────────────┘
                                                  │
                                                  ▼
                        [Docker & Docker Compose Orchestration]
                                                  │
                                                  ▼
                        [Pytest Suite (12 Tests Passing) & GitHub Actions]
```

---

## 📊 Measured Benchmark Results (Out-of-Sample Test Partition)

Evaluation conducted on unseen test data (November 9, 2023 – December 31, 2023):

| Model Architecture | Model Category | Test RMSE (\$) | Test MAE (\$) | Test MAPE (%) | WAPE (%) | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gated Recurrent Unit (GRU)** | **Deep Learning (Recurrent)** | **\$775.31** | **\$605.79** | **54.25%** | **38.09%** | **⭐ CHAMPION** |
| **Bidirectional LSTM** | Deep Learning (Recurrent) | \$791.72 | \$624.81 | 52.57% | 39.29% | Runner-Up |
| **Vanilla LSTM** | Deep Learning (Recurrent) | \$802.62 | \$631.79 | 50.75% | 39.73% | Stable |
| **ARIMA(1, 0, 1)** | Classical Statistical | \$764.10 | \$607.74 | 55.69% | 38.22% | Statistical Baseline |
| **7-Day Moving Average** | Classical Baseline | \$845.53 | \$673.82 | 69.81% | 42.37% | Trailing Baseline |
| **Naïve Persistence ($y_{t-1}$)**| Classical Baseline | \$1,045.73 | \$880.21 | 83.15% | 55.35% | Lag Baseline |

---

## 📁 Repository Directory Hierarchy

```
d:\The Developers Arena\
├── data/
│   ├── raw/                 # Immutable datasets (supermarket_sales.csv, customer_churn.csv)
│   ├── interim/             # Continuous daily aggregated series (daily_supermarket_sales.csv)
│   └── processed/           # 3D sequence tensors (X_train.npy, y_train.npy, etc.)
├── src/
│   ├── data_processing/     # Preprocessor pipeline, lag generation, scaling
│   ├── models/              # Model architectures (LSTM, GRU, BiLSTM, baselines, churn)
│   ├── training/            # Checkpointing, early stopping, model selection
│   ├── api/                 # High-performance FastAPI application
│   └── monitoring/          # Drift detection (KS test, Population Stability Index)
├── dashboard/
│   └── app.py               # Enterprise Streamlit analytics application
├── docker/
│   ├── Dockerfile.api       # Multi-stage container for API
│   ├── Dockerfile.dashboard # Container for Streamlit
│   └── docker-compose.yml   # Multi-service orchestration
├── tests/                   # 12 automated Pytest unit and integration tests
├── deployment/              # Kubernetes Deployment, Service & HPA manifests
├── docs/                    # Mathematical foundations, technical reports, cloud guides
├── artifacts/
│   ├── models/              # Serialized neural weights (champion_model.h5)
│   ├── scalers/             # Fitted MinMax scalers (feature_scaler.pkl)
│   ├── figures/             # 7 high-resolution diagnostic & forecast plots
│   └── metrics/             # JSON reports for baselines, DL results, and drift
├── requirements.txt         # Pinned production dependencies
└── README.md                # System documentation
```

---

## 🚀 Quickstart Guide (Windows 11 Execution)

### 1. Environment & Dependencies Installation
Open PowerShell in the project directory:
```powershell
cd "d:\The Developers Arena"

# Install pinned dependencies
python -m pip install -r requirements.txt
```

### 2. Run the Full End-to-End Pipeline
Execute each stage sequentially or verify with the automated scripts:

```powershell
# Step 1: Environment and raw dataset validation
python scripts/validate_environment_and_data.py

# Step 2: Exploratory Data Analysis & Stationarity Testing
python src/data_processing/eda_diagnostics.py

# Step 3: Feature Engineering, Chronological Splitting & Sequence Tensors
python src/data_processing/preprocessor.py

# Step 4: Classical Baseline Benchmarking (Naïve, Moving Average, ARIMA)
python src/models/baseline_models.py

# Step 5: Deep Learning Training & Champion Model Selection
python src/training/train_pipeline.py

# Step 6: Optional Customer Churn Classification Module
python src/models/churn_classifier.py

# Step 7: Statistical Data Drift Detection
python src/monitoring/drift_detector.py
```

### 3. Run Automated Tests
```powershell
pytest -v tests/
```
Expected Output: `12 passed in ~17s` (100% pass rate).

### 4. Launch the FastAPI Serving Microservice
```powershell
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```
- Interactive Swagger API Documentation: `http://localhost:8000/docs`
- Redoc API Documentation: `http://localhost:8000/redoc`
- Health Diagnostic: `http://localhost:8000/health`

### 5. Launch the Streamlit Analytics Dashboard
```powershell
streamlit run dashboard/app.py
```
- Access interactive web UI at: `http://localhost:8501`

---

## 🐳 Docker Container Orchestration

Run the entire multi-service microservice stack with Docker Compose:
```bash
docker-compose up --build -d
```
- FastAPI container running on port `8000`
- Streamlit dashboard container running on port `8501`

---

## 📬 API Usage Example

### Predict Next-Day Sales (`POST /predict`)
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "history_sales": [1200.0, 1350.0, 1100.0, 1450.0, 1600.0, 1800.0, 1950.0,
                      1250.0, 1300.0, 1400.0, 1550.0, 1650.0, 1850.0, 2100.0],
    "is_weekend": 1,
    "day_of_week": 5,
    "month": 12
  }'
```

**Response (HTTP 200 OK)**:
```json
{
  "predicted_sales": 1265.06,
  "confidence_interval_80": [272.67, 2257.46],
  "confidence_interval_95": [0.0, 2784.67],
  "model_name": "GRU_Champion_Forecaster",
  "status": "SUCCESS",
  "execution_time_ms": 142.3
}
```

---

## 👨‍💻 Project Contributor & Mentor
- **Specialization**: Time Series Forecasting using Deep Learning (LSTM/GRU)
- **Frameworks**: TensorFlow, Keras, PyTorch, Scikit-Learn, Statsmodels, FastAPI, Streamlit, Docker
