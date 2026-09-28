
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = os.environ.get("ZORO_API_BASE_URL")

if not API_BASE_URL:
    raise RuntimeError("Backend API not set.")
