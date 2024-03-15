import os
from dotenv import load_dotenv
import logging
import json

from bot.stress_data import StressData
from bot.language import Language

# Get environment settings from .env file
load_dotenv()
TOKEN = os.getenv("SECRET_TOKEN")
YANDEX_GPT_API_KEY = os.getenv("YANDEX_TOKEN")
YANDEX_CATALOG = os.getenv("YANDEX_CLOUD_CATALOG")
SYSTEM_PROMPT = "Ты - репетитор для подготовки к ЕГЭ, которое проводится в конце мая среди школьников 11 классов. \
  Экзамен будет проводиться через два с половиной месяца. Распиши план обучения для ученика среднего уровня знаний"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

stress_data = StressData.from_file("data/raw.txt")
language = Language
