import telegram
import os, sys
from flask import Flask, request, render_template
import json
import logging
import subprocess
from urllib import parse

#sys.path.append(os.path.abspath(os.path.join('..')))

from modules.messager import Messager, MY_CHAT_ID

#TODO Store key in database
MY_TELEGRAM_KEY="1697098452:AAE6Jq-dlO0vMyOQdxgzqTEZV3K-5LpkNWo"

class TelegramWebhookBot(object):
    def __init__(self):
        self.key = MY_TELEGRAM_KEY
        self.bot = telegram.Bot(token=self.key)
        self.https_app = Flask(__name__, template_folder='../templates')
        self.cmd_queue = queue.Queue(maxsize=20)

        @self.https_app.route('/')
        def index(): #TODO fix issue of register by template
            logging.info('Registered webhok succesfully')
            return render_template('upload_cert.html')

        @self.https_app.route('/webhook', methods=['POST'])
        def webhook_handler(self=self):
            try:
                logging.info("Method: %s" % request.method)
                if request.method == "POST":
                    # retrieve the message in JSON and then transform it to Telegram object
                    update = telegram.Update.de_json(request.get_json(force=True), self.bot)

                    messager = Messager(update)
                    chat_id, result = messager.parse_command()
                if chat_id and result:
                    logging.debug("[webhook_handler] chat_id=%s, result=%s", chat_id, hex(result))
                    self.cmd_queue.put(str(result) + "@" + str(chat_id))
                elif chat_id:
                    self.send_message(chat_id, "Command is not recognized.")
                else:
                    logging.error("[Error] Request message wrong format")
            except Exception as e: # work on python 3.x
                logging.error('[Exception][webhook_handler]: '+ str(e))

            return 'ok'

        @self.https_app.route("/getcmd", methods=['GET'])
        def get_cmd(self=self):
            pass

        @self.https_app.route("/sendcmd", methods=['POST'])
        def send_cmd(self=self):
            pass

    def send_message(self, chat_id, result):
        self.bot.sendMessage(chat_id=chat_id, text=result)

    def run(self):
        logging.info("Please access https:<domain>/ to register webhook portal for udpates!")
        self.https_app.run(host='0.0.0.0', port='443', ssl_context=('ssl/public.pem', 'ssl/private.key'))
        #self.https_app.run(host='10.148.0.7', port='80')