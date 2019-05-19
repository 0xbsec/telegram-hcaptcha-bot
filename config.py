import os
from dotenv import load_dotenv

load_dotenv()

APP_URL = os.getenv('APP_URL')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_USERNAME = os.getenv('TELEGRAM_USERNAME')
HCAPTCHA_SECRET = os.getenv('HCAPTCHA_SECRET')
HCAPTCHA_POST_URI = os.getenv('HCAPTCHA_POST_URI')
HCAPTCHA_SITE_KEY = os.getenv('HCAPTCHA_SITE_KEY')