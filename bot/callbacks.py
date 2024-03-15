from telegram import Update
from telegram.ext import ContextTypes
from bot.config import logger, stress_data, language
from random import choice


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task = stress_data.generate_task()
    await update.message.reply_text(choice(language.intro).format(task=task))


async def wildcard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    word = update.message.text.strip()
    case_map = list(map(str.isupper, word))
    if any(case_map[1:]) and case_map[0]:
        word = word[0].lower() + word[1:]

    if stress_data.contains(word):
        if stress_data.is_correct(word):
            task = stress_data.generate_task()
            praise = language.visual_praise
            await update.message.reply_text(
                choice(language.right_answer).format(task=task, praise=praise),
                parse_mode="Markdown",
            )

        else:
            task = stress_data.generate_task()
            right_answer = stress_data.stress(word)
            await update.message.reply_text(
                choice(language.wrong_answer).format(
                    right_answer=right_answer, task=task
                ),
                parse_mode="Markdown",
            )

    else:
        task = stress_data.generate_task()
        await update.message.reply_text(
            choice(language.wildcard).format(task=task),
            parse_mode="Markdown",
        )
