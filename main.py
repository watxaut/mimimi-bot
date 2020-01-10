import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackQueryHandler

import bot.main as bot
from bot.secret import TELEGRAM_TOKEN

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    logger = logging.getLogger(__name__)

    # telegram bot init
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # adds the functions to the bot function
    dispatcher.add_handler(CommandHandler("start", bot.start))
    dispatcher.add_handler(CommandHandler("language", bot.choose_language))
    dispatcher.add_handler(MessageHandler(filters.Filters.voice, bot.input_received))
    dispatcher.add_handler(MessageHandler(filters.Filters.text, bot.input_received))

    # button rating
    dispatcher.add_handler(CallbackQueryHandler(bot.response))

    logger.info("--- Starting bot ---")

    # starts receiving calls
    updater.start_polling(timeout=10)
    updater.idle()
