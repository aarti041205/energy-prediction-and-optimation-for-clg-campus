# ⚡ Machine Learning + GenAI Energy Prediction & Optimization System

> **A Production-Grade Smart Campus Infrastructure System powered by Machine Learning, Google Gemini RAG, FastAPI, Streamlit, PostgreSQL, and AWS Cloud.**

---

## 🏗️ System Architecture

```mermaid
graph TD
    User[User / Campus Engineer] -->|HTTP / Streamlit UI| Streamlit[Streamlit Dashboard (Port 8501)]
    Streamlit -->|REST API Requests| FastAPI[FastAPI REST API (Port 8000)]
    
    subgraph Core ML & AI Services
        FastAPI -->|Lifespan Load ONCE| RF[Random Forest ML Regressor]
        FastAPI -->|Anomaly Detection| IF[Isolation Forest Detector]
        FastAPI -->|RAG Vector Search| FAISS[FAISS Vector DB (Top-5 Chunks)]
        FAISS -->|LLM Synthesis| Gemini[Google Gemini 3.6 Flash]
    end
    
    subgraph Data & Storage Layer
        FastAPI -->|SQLAlchemy ORM| Postgres[(PostgreSQL / Amazon RDS)]
        FastAPI -->|PDF/DOCX/MD Export| ReportGen[Report Generator Engine]
    end

    subgraph Intelligent Alert System
        FastAPI -->|10 Alert Criteria| AlertEngine[Alert Engine]
        AlertEngine -->|Critical Severity| SMTP[SMTP Email Dispatcher]
    end
```

---

## ✨ Features & Capabilities

- **⚡ Single-Instance ML Load Prediction**: Trained Random Forest Regressor loaded **ONCE** at startup via FastAPI lifespan context manager. Computes confidence score, timestamp, cost, carbon footprint, and stores telemetry in PostgreSQL.
- **📊 Analytics & Multi-Tab Dashboard**: Interactive Plotly visualizations for daily, weekly, monthly, and yearly consumption, building comparison, cost share, carbon footprint, heatmap, weather impact, and solar contribution.
- **💡 9-Point Energy Optimization Engine**: Provides actionable recommendations for HVAC setpoints, peak load shifting, lighting, equipment scheduling, solar PV utilization, and battery storage with annual savings calculations.
- **🚨 10-Rule Intelligent Alert Engine**: Automatically evaluates 10 real-time alert rules (High Energy, Peak Demand, Abnormal Equipment Load, Carbon Emission, Cost, Equipment Failure Probability, Temperature Threshold, Occupancy Overload, Solar Output Drop, Anomaly Detection).
- **📧 Automated Email Notifications**: Dispatches HTML formatted email notifications to facility engineers for **Critical** severity alerts via SMTP background tasks.
- **🤖 Advanced Gemini RAG Chatbot**: FAISS vector store with top-5 chunk retrieval, conversation memory, confidence scores, and source citations.
- **📄 AI Executive Report Generation**: Synthesizes 10-section executive reports using Gemini and exports to **PDF** (`reportlab`), **DOCX** (`python-docx`), and **Markdown**.
- **📥 Multi-Format Data Exports**: Native CSV and Excel export support across Predictions, Analytics, Optimization, and Anomaly logs.
- **☁️ AWS Cloud Production Ready**: Fully equipped with Docker, Docker Compose, Nginx reverse proxy, Systemd unit files, GitHub Actions CI/CD workflow, and automated EC2 setup scripts.

---

## 🛠️ Project Structure

```
Energy-Prediction-Optimization-System/
├── dashboard/                 # Streamlit UI Application
│   ├── app.py                 # Main Dashboard Page
│   ├── api_client.py          # Centralized FastAPI HTTP Communication Helper
│   ├── dashboard_utils.py     # Data aggregators & metrics
│   └── pages/                 # Multi-Page Dashboard Views
│       ├── 🔮_Energy_Prediction.py
│       ├── 📊_Analytics.py
│       ├── 💡_Energy_Optimization.py
│       ├── 🚨_Anomaly_Detection.py
│       ├── 🤖_AI_Assistant.py
│       └── ⚙️_Settings.py
├── src/                       # Backend Source Modules
│   ├── api/                   # FastAPI Application & Routes
│   │   ├── app.py             # REST API Definition (13 Endpoints)
│   │   ├── predictor.py       # Single-Instance Model Manager
│   │   └── schemas.py         # Pydantic Input/Output Schemas
│   ├── anomaly/               # Alert Engine & Anomaly Detection
│   │   ├── alert_engine.py    # 10-rule alert evaluator
│   │   └── detect.py          # Isolation Forest model pipeline
│   ├── config/                # Centralized Config & Parameters
│   │   └── config.py
│   ├── database/              # SQLAlchemy Database ORM
│   │   ├── db_connection.py   # Connection Manager & Health Checks
│   │   └── models.py          # ORM Models (Predictions, Alerts, Chat, Reports)
│   ├── optimization/          # Savings & Recommendation Engine
│   │   └── recommendations.py
│   ├── rag/                   # RAG Chatbot Engine
│   │   ├── chatbot.py         # Top-5 FAISS + Gemini LLM pipeline
│   │   └── prompts.py         # System prompt templates
│   └── utils/                 # Utilities & Generators
│       ├── email_service.py   # SMTP HTML email dispatcher
│       ├── logger.py          # Rotating file logging handler
│       └── report_generator.py # PDF / DOCX / MD Exporter
├── deployment/                # AWS Infrastructure & DevOps
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── fastapi.service
│   ├── streamlit.service
│   ├── setup_ec2.sh
│   └── DEPLOYMENT_GUIDE.md
├── tests/                     # Pytest Unit & Integration Test Suite
├── docker-compose.yml         # Container Orchestration
├── requirements.txt           # Production Dependencies
└── .env.example               # Environment Variables Template
```

---

## 🔌 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API Welcome Status |
| `GET` | `/health` | System & Database Health Check |
| `POST` | `/predict` | ML Load Prediction + Alert Evaluation + DB Save |
| `POST` | `/chat` | Gemini RAG Chatbot Q&A |
| `GET` | `/analytics` | Aggregated Campus Energy & Cost Analytics |
| `POST` | `/optimize` | 9-Point Optimization Recommendation Engine |
| `POST` | `/anomaly` | Isolation Forest Anomaly Detection |
| `GET` | `/alerts` | Query System Alerts with Filtering |
| `POST` | `/alerts/{id}/acknowledge` | Acknowledge Alert in DB |
| `POST` | `/generate-report` | Synthesize & Export AI PDF/DOCX/MD Report |
| `GET` | `/prediction-history` | Fetch Historical Prediction Records |
| `GET` | `/download-report` | Download Generated PDF/DOCX/MD Files |
| `GET` | `/export-csv` | Export Telemetry Data as CSV |
| `GET` | `/export-excel` | Export Telemetry Data as Excel |

---

## 🚀 Local Setup & Execution Guide

### 1. Prerequisites
- Python 3.10+
- PostgreSQL (Optional; fallback SQLite database activates automatically if PostgreSQL is offline)

### 2. Environment Setup
```bash
# Clone Repository
git clone https://github.com/your-username/Energy-Prediction-Optimization-System.git
cd Energy-Prediction-Optimization-System

# Create Virtual Environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Configure Environment Variables
cp .env.example .env
```

### 3. Run FastAPI Backend
```bash
uvicorn src.api.app:app --host 127.0.0.1 --port 8000 --reload
```
*API Swagger Documentation will be available at `http://127.0.0.1:8000/docs`.*

### 4. Run Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```
*Streamlit Dashboard will launch at `http://localhost:8501`.*

---

## 🧪 Running Automated Tests
```bash
python -m pytest tests/ -v
```

---

## ☁️ AWS Production Deployment

For complete instructions on deploying to **AWS EC2**, **Amazon RDS (PostgreSQL)**, **Amazon S3**, **CloudWatch**, and **Let's Encrypt SSL**, please refer to the [AWS Deployment Guide](file:///c:/Users/LENOVO/OneDrive/Desktop/Energy-Prediction-Optimization-System/deployment/DEPLOYMENT_GUIDE.md).

```bash
# Docker Compose Local/Cloud Deployment
docker-compose up --build -d
```

---

## 📜 License & Acknowledgments
Developed for Smart College Campus Infrastructure & Energy Optimization.
© 2026 Energy Prediction and Optimization System.
