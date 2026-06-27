import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cloudpulse-dev-key')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    APP_PORT = int(os.environ.get('APP_PORT', 5000))
    
    # Metrics refresh interval in seconds
    METRICS_INTERVAL = 5
    
    # Alert thresholds
    CPU_THRESHOLD = 80
    MEMORY_THRESHOLD = 85
    DISK_THRESHOLD = 90