import os
import telebot

api_key = os.getenv('CODESHED_BOT_TOKEN')
bot = telebot.TeleBot(api_key)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)



bot.infinity_polling()