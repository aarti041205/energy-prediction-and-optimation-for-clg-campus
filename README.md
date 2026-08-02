# ⚡ Smart Campus Energy Prediction & Optimization System

A full-stack machine learning and GenAI project for predicting campus energy consumption, detecting anomalies, recommending optimizations, and supporting smarter facility decisions.

## 🧠 Description
This project helps universities and facility teams monitor building energy usage more effectively. It combines a Streamlit dashboard, FastAPI backend, predictive models, anomaly detection, optimization recommendations, and an AI assistant powered by RAG to turn energy data into actionable insights.

## ✨ Features
- Predicts energy consumption using machine learning
- Detects abnormal energy patterns and alerts users
- Recommends optimization actions to reduce waste and costs
- Includes an AI chatbot for energy-related questions
- Provides dashboards and reports for analytics and decision-making

## 🛠️ Installation
1. Clone the repository
```bash
git clone https://github.com/your-username/Energy-Prediction-Optimization-System.git
cd Energy-Prediction-Optimization-System
```

2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
```

## ▶️ Usage
Run the backend:
```bash
uvicorn src.api.app:app --host 127.0.0.1 --port 8000 --reload
```

Run the dashboard:
```bash
streamlit run dashboard/app.py
```

Open the API docs at:
```text
http://127.0.0.1:8000/docs
```

## 📂 Project Structure
- dashboard/ - Streamlit UI and page components
- src/api/ - FastAPI routes and request schemas
- src/models/ - training and prediction logic
- src/anomaly/ - anomaly detection engine
- src/optimization/ - optimization recommendations
- src/rag/ - AI assistant and retrieval pipeline
- reports/ and saved_models/ - generated outputs and trained models

## 📸 Screenshots
Add screenshots or GIFs here for:
- Dashboard overview
- Energy analytics page
- AI assistant chat view
- Optimization recommendations

## 🤝 Contributing
Contributions are welcome. Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request with a clear description

## 📜 License
This project is licensed under the MIT License.

## 👤 Author
Your Name
- GitHub: https://github.com/your-username
- LinkedIn: https://www.linkedin.com/in/your-username
