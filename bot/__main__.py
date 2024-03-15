from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Application,
)
from telegram.ext.filters import TEXT
from telegram import Bot, BotCommand

from bot.config import TOKEN
from bot.callbacks import *
from bot.db.commands import create_tables


async def bot_setup(application) -> None:
    await application.bot.set_my_commands(
        [
            BotCommand("start", "Сгенерировать первое задание"),
        ]
    )


def main() -> None:
    create_tables()

    application = ApplicationBuilder().token(TOKEN).post_init(bot_setup).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(TEXT, message_handler))

    application.run_polling()


if __name__ == "__main__":
    main()
