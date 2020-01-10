import json
import logging
from pathlib import Path

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import mimimitifyer.main
from mimimitifyer.config import d_lang

logger = logging.getLogger(__name__)


def write_json_users(user_id, language):
    path_json = Path(".") / "users/users.json"
    f = open(path_json, "r")
    json_users = json.load(f)
    f.close()
    json_users[user_id] = language
    f = open(path_json, "w")
    json.dump(json_users, f)
    f.close()


def read_language_user(user_id):
    path_json = Path(".") / "users/users.json"
    f = open(path_json, "r")
    json_users = json.load(f)
    f.close()
    return json_users[user_id]


def choose_language(bot, update):
    first_name = update.message.chat.first_name

    start_reply = f"Hello {first_name}! Choose your language:"
    keyboard = [InlineKeyboardButton(text=lang, callback_data=code) for lang, code in d_lang.items()]
    reply_markup = InlineKeyboardMarkup([keyboard])

    update.message.reply_text(start_reply, reply_markup=reply_markup)


def start(bot, update):
    logger.info("New user logged in")
    choose_language(bot, update)


def input_received(bot, update):
    user_id = str(update.message.chat.id)
    if update.message.text is not None:
        logger.info("Text input received")
        language = read_language_user(user_id)
        text_i = mimimitifyer.main.change_all_vowels(update.message.text)
        file_i = mimimitifyer.main.text_to_speech(text_i, language)
    elif update.message.voice is not None:
        logger.info("Voice input received")
        language = read_language_user(user_id)
        audio_file_path = update.message.voice.get_file()['file_path']
        file_i, text_i = mimimitifyer.main.mimimitify(audio_file_path, language=language)

    else:
        update.message.reply_text('No understando')
        return

    bot.send_message(update.message.chat_id, text_i)
    bot.send_audio(update.message.chat_id, audio=open(file_i, 'rb'))


def response(bot, update) -> None:
    user_id = str(update.callback_query.from_user.id)
    bot_message = update.callback_query.message.text
    language = update.callback_query.data

    if "Choose your language" in bot_message:
        write_json_users(user_id, language)
    else:
        update.message.reply_text('No understando response')
