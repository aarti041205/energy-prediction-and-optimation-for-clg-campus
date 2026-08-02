import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DATA = DATA_DIR / "raw" / "campus_energy.csv"
PROCESSED_DATA = DATA_DIR / "processed" / "campus_energy_features.csv"
PROCESSED_ALT_DATA = DATA_DIR / "processed" / "campus_energy_processed.csv"

MODEL_DIR = BASE_DIR / "saved_models"
MODEL_DIR.mkdir(exist_ok=True)

RANDOM_FOREST_MODEL = MODEL_DIR / "random_forest_model.pkl"
ALT_RANDOM_FOREST_MODEL = MODEL_DIR / "random_forest.pkl"
DEPLOYMENT_MODEL = MODEL_DIR / "deployment_model.pkl"
ANOMALY_MODEL = MODEL_DIR / "anomaly_detector.pkl"
PREPROCESSOR = MODEL_DIR / "preprocessing_pipeline.pkl"

VECTOR_DB_DIR = BASE_DIR / "vector_db"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

VECTOR_DB_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Database Settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "campus_energy")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# SMTP Settings for Email Notifications
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "alerts@campusenergy.ai")
RECIPIENT_EMAILS = [
    e.strip() for e in os.getenv("RECIPIENT_EMAILS", "facility@campus.edu").split(",") if e.strip()
]

# AI / Gemini Settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

# Optimization & Financial Parameters
PRICE_PER_KWH = 8.5          # ₹ per kWh
CARBON_PER_KWH = 0.82        # kg CO2 per kWh

# Alert Thresholds
HIGH_ENERGY_THRESHOLD = 400.0      # kWh
PEAK_DEMAND_THRESHOLD = 450.0       # kWh
HIGH_EQUIPMENT_LOAD = 0.85          # ratio
HIGH_CARBON_THRESHOLD = 300.0       # kg CO2
HIGH_COST_THRESHOLD = 3000.0        # ₹
HIGH_TEMP_THRESHOLD = 38.0          # °C
HIGH_OCCUPANCY_THRESHOLD = 400      # count
LOW_SOLAR_THRESHOLD = 50.0          # kW