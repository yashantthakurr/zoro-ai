
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = os.environ.get("ZORO_API_BASE_URL")
# API_BASE_URL = os.environ.get("ZORO_API_BASE_URL") or "http://localhost:8000/api/v1"

if not API_BASE_URL:
    raise RuntimeError("Backend API not set.")
