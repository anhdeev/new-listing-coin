import telegram
from telegram import ParseMode

#TODO Store key via env
MY_TELEGRAM_KEY="1697098452:AAE6Jq-dlO0vMyOQdxgzqTEZV3K-5LpkNWo"
MY_CHAT_ID='@newlistingtoken'

class TeleBot(object):
    def __init__(self):
        self.key = MY_TELEGRAM_KEY
        self.bot = telegram.Bot(token=self.key)
        self.updater = None # TODO

    def send(self, msg, html=False):
        self.bot.sendMessage(chat_id=MY_CHAT_ID, text=msg, parse_mode=ParseMode.HTML if html else ParseMode.MARKDOWN)