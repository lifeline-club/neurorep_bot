from enum import Enum
from random import choice
import json
from telegram import Update, Bot
from telegram.ext import ContextTypes

from bot.config import language
from bot.db.repo import Repo

repo = Repo()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(choice(language.intro))
    repo.users.update_user_state(
        user_id=update.message.from_user.id, state=1
    )


async def choose_track(update: Update, user_id: int, text: str) -> None:
    meta = ""
    text = text.strip().lower()
    match text:
        case "математика":
            await update.message.reply_text(f"Предмет {text} найден")
            return {"meta": {
                'choosed_track': 'Математика'
            }}
        case "русский язык":
            await update.message.reply_text(f"Предмет {text} найден")
            return {"meta":
                    {'choosed_track': 'Русский язык'}
                }
        case _:
            await update.message.reply_text(f"Предмет {text} не найден")
            return {"meta": {}}


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
            await start()
        case 1:
            meta = choose_track(update, user_id, text)["meta"]
            repo.users.update_user_state(user_id, state=2, meta=json.dumps(meta))

