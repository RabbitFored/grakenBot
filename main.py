import os
from Crypto.Cipher import AES
import base64
import logging

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    MessageHandler,
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext,
)

# Enable logging
from telegram.utils import helpers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    usr_cmd = update.message.text.split("_")[-1]
    if usr_cmd == "/start":
        context.bot.sendMessage(chat_id=update.message.chat.id,
                                text='Hi, I am Graken. I can store all your files in a safe ship.')
    else:
        try:
            file_d = usr_cmd
            key = 'I am inevitable.'
            iv = '1NfaItAqnACMk45O'
            decryption_suite = AES.new(key, AES.MODE_CFB, iv)
            file_id = decryption_suite.decrypt(base64.b64decode(file_d))
            sendFile = context.bot.forward_message(chat_id=update.message.from_user.id, from_chat_id="",
                                                   message_id=int(file_id))
        except:
            context.bot.sendMessage(chat_id=update.message.chat.id, text='File Not Found')


def graken(update, context):
    if update.message.chat.type == "private":
        editable = update.message.reply_text("Please wait ...")
        try:
            forwarded = context.bot.copy_message(chat_id='',
                                                 from_chat_id=update.message.chat.id,
                                                 message_id=update.message.message_id)

            context.bot.copy_message(chat_id='',
                                     from_chat_id=update.message.chat.id,
                                     message_id=update.message.message_id)
            file_er_id = forwarded.message_id
            key = '7I am inevitable.7'
            iv = '71NfaItAqnACMk45O7'
            enc_s = AES.new(key, AES.MODE_CFB, iv)
            cipher_text = enc_s.encrypt(str(file_er_id))
            encoded_cipher_text = base64.b64encode(cipher_text)
            sharelink = f"https://telegram.dog/iconrails_bot?start=graken_{(str(encoded_cipher_text))[2:-1]}"
            context.bot.sendMessage(chat_id='@grakenBot', text=f"Done\n{forwarded.message_id}",
                                    reply_to_message_id=forwarded.message_id)
            context.bot.editMessageText(f"File stored safely in  a safest place, get it anytime using :\n\n{sharelink}",
                                        chat_id=update.message.chat_id,
                                        message_id=editable.message_id)
        except:
            context.bot.sendMessage(chat_id=update.message.chat.id, text='Something went wrong')


def main():
    TOKEN = ""
    updater = Updater(TOKEN)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler((Filters.audio | Filters.document | Filters.video), graken))
    updater.start_polling()


if __name__ == "__main__":
    main()
