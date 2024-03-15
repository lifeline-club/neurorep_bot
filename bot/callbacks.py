from enum import Enum
from random import choice
import json
from telegram import Update, Bot
from telegram.ext import ContextTypes

from bot.config import language
from bot.db.repo import Repo

import time
import requests
import json

from bot.config import YANDEX_GPT_API_KEY, YANDEX_CATALOG, SYSTEM_PROMPT

repo = Repo()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(choice(language.intro))
    repo.users.update_user_state(
        user_id=update.message.from_user.id, state=1
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(choice(language.about))


async def choose_track(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> dict:
    text = text.strip().lower()
    match text:
        case "математика":
            return {"meta": {
                'choosed_track': 'Математика'
            }}
        case "русский язык":
            return {"meta":
                    {'choosed_track': 'Русский язык'}
                }
        case _:
            await update.message.reply_text(f"Предмет {text} не найден")
            return {"meta": {'choosed_track': ""}}



async def subject_selection(subject: str):
    body = {
        "modelUri": f"gpt://{YANDEX_CATALOG}/{"yandexgpt-lite"}",
        "completionOptions": {"stream": False, "temperature": 0, "maxTokens": "2000"},
        "messages": [
            {"role": "system", "text": SYSTEM_PROMPT},
            {"role": "user", "text": subject},
        ],
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_GPT_API_KEY}",
        "x-folder-id": YANDEX_CATALOG,
    }

    response = requests.post(url, headers=headers, json=body)
    response_json = json.loads(response.text)
    operation_id = response_json["id"]

    url = f"https://llm.api.cloud.yandex.net/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {YANDEX_GPT_API_KEY}"}

    done = False
    while not done:
        response = requests.get(url, headers=headers)
        response_json = json.loads(response.text)
        done = response_json["done"]
        time.sleep(1)

    if response.status_code != 200:
        return "ERROR"

    answer = response_json["response"]["alternatives"][0]["message"]["text"]

    return answer


class States(Enum):
    START = 0
    CHOOSE_TRACK = 1
    CHOOSED_TRACK = 2


async def message_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = update.message.from_user.id
    text = update.message.text

    state = repo.users.get_user_state(user_id)

    match state["state"]:
        case 0:
            await start(update, context)
        case 1:
            meta = await choose_track(update, user_id, text)
            meta = meta["meta"]
            repo.users.update_user_state(user_id, state=10 if meta["choosed_track"] == "Математика" else 2, meta=json.dumps(meta))
            to_send = await subject_selection(meta["choosed_track"])
            await update.message.reply_text(to_send)
            if meta["choosed_track"] == "Математика":
                task_to_send = """
Конкурс исполнителей проводится в 5 дней. Всего заявлено 80 выступлений — по одно-
му от каждой страны, участвующей в конкурсе. Исполнитель из России участвует в конкурсе.
В первый день запланировано 8 выступлений, остальные распределены поровну между остав-
шимися днями. Порядок выступлений определяется жеребьёвкой. Какова вероятность, что
выступление исполнителя из России состоится в третий день конкурса?
"""
            else:
                task_to_send = """
Расставьте знаки препинания. Укажите номера предложений, в которых нужно поставить ОДНУ запятую.
1) Туч на небе не было и солнце не выглядывало.
2) Видеть её можно было ежедневно то с бидоном то с сумкой то с сумкой и бидоном вместе.
3) Жёлтые листья и утренние туманы напоминали об ушедшем лете.
4) Весь день идёт снег либо дождь со снегом.
5) Надежда с упреком взглянула прямо на Курочкина и тот замолчал.
"""
            await update.message.reply_text(task_to_send)
        case 2:
            if text == "15" or text == "51":
                await update.message.reply_text("Поздравляю! Ответ 15 правильный!")
                task_to_send = """
Укажите варианты ответов, в которых в обоих словах одного ряда пропущена одна и та же буква. Запишите номера ответов.
1) (пациенты) леч..тся, маяч..щий (вдали лес)
2) завис..шь, подстриж..нный
3) бор..шься, воспева..мый
4) проед..шься, необита..мый
5) верт..шься, обнаруж..нный
"""
                await update.message.reply_text(task_to_send)
                repo.users.update_user_state(user_id, state=3)
            else:
                await update.message.reply_text("Неправильный ответ. Попробуйте ещё раз.")
        case 3:
            if text in ["134", "143", "314", "341", "412", "421"]:
                await update.message.reply_text("Поздравляю! Ответ 134 правильный!")
                task_to_send = """
Отредактируйте предложение: исправьте лексическую ошибку, исключив лишнее слово. Выпишите это слово.
Опираясь на огромную базу синонимичных значений, сайт выдаст все возможные поисковые вариативные версии.
"""
                await update.message.reply_text(task_to_send)
                repo.users.update_user_state(user_id, state=4)
            else:
                await update.message.reply_text("Неправильный ответ. Попробуйте ещё раз.")
        case 4:
            if text.lower().strip() == "вариативные":
                await update.message.reply_text("Поздравляю! Ответ вариативные правильный!")
                task_to_send = """
Укажите варианты ответов, в которых в обоих словах одного ряда пропущена одна и та же
буква. Запишите номера ответов.
1) влюбч..вый, заботл..вый
2) подмиг..вавший, исслед..вать
3) удоста..вавший, мал..вать
4) рул..вой, глянц..витая
5) отча..ться, воробуш..к
"""
                await update.message.reply_text(task_to_send)
                repo.users.update_user_state(user_id, state=0)
            else:
                await update.message.reply_text("Неправильный ответ. Попробуйте ещё раз.")
        case 10:
            if text in ["0,225", "0.225"]:
                await update.message.reply_text("Поздравляю! Ответ 0,225 правильный!")
                task_to_send = """
По двум параллельным железнодорожным путям друг навстречу другу следуют скорый и
пассажирский поезда, скорости которых равны соответственно 65 км/ч и 35 км/ч. Длина пас-
сажирского поезда равна 700 метрам. Найдите длину скорого поезда, если время, за которое
он прошел мимо пассажирского поезда, равно 36 секундам. Ответ дайте в метрах.
"""
                await update.message.reply_text(task_to_send)
                repo.users.update_user_state(user_id, state=0)
            else:
                await update.message.reply_text("Неправильный ответ. Попробуйте ещё раз.")
        

