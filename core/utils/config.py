from os import getenv
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = getenv("BOT_TOKEN")
ALERTS_TOKEN = getenv("ALERTS_TOKEN")
DORM_CHAT_ID = getenv("DORM_CHAT_ID")
WEBHOOK_SECRET = getenv("WEBHOOK_SECRET")
BASE_WEBHOOK_URL = getenv("BASE_WEBHOOK_URL")
WEB_SERVER_HOST = getenv("WEB_SERVER_HOST")
TEST_CHAT_ID = getenv("TEST_CHAT_ID")
DORM_CHAT_ID = getenv("DORM_CHAT_ID")
ADMIN_ID = getenv("ADMIN_ID")
ADMIN_IDS = list(map(int, ADMIN_ID.split(", ")))
ALINA_ID = int(getenv("ALINA_ID"))
