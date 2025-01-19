import os
import telebot

api_key = os.getenv('CODESHED_BOT_TOKEN')
bot = telebot.TeleBot(api_key)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "I am just a simple bot figuring out what can I help people with.")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)



bot.infinity_polling()