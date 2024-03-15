from random import choice
from telegram import Update
from telegram.ext import ContextTypes

from bot.config import logger, stress_data, language
from bot.db.repo import Repo

repo = Repo()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task = stress_data.generate_task()
    await update.message.reply_text(choice(language.intro).format(task=task))


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    text = update.message.text

    state = repo.users.get_user_state(user_id)
