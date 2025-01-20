import os
import telebot
import requests
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

api_key = os.getenv('CODESHED_BOT_TOKEN')
bot = telebot.TeleBot(api_key)

# Set bot commands for inbuilt menu
bot.set_my_commands([
    telebot.types.BotCommand("start", "Start the bot"),
    telebot.types.BotCommand("hello", "Say hello"),
    telebot.types.BotCommand("help", "Get help"),
    telebot.types.BotCommand("quote", "Receive quotes")
])

# /start and /hello command handler
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    welcome_msg = (
        "🌟 **Hello! Welcome to the Hindi Quotes Bot!** 🌟\n\n"
        "📜 Get ready to explore inspirational and meaningful Hindi quotes.\n\n"
        "✨ Use /help to see all the amazing features and commands you can try!\n"
    )
    bot.reply_to(message, welcome_msg, parse_mode='Markdown')

# /help command handler
@bot.message_handler(commands=['help'])
def send_help(message):
    helpmsg = (
        "🛠️ **Here's how I can help you:**\n\n"
        "➡️ **/start** - Begin using the bot and explore its features.\n"
        "➡️ **/hello** - Say hello and connect with the bot.\n"
        "➡️ **/quote** - Stay tuned for inspiring and meaningful Hindi quotes!\n\n"
        "💡 Let me know if you need anything else. I'm here to assist! 😊"
    )
    bot.reply_to(message, helpmsg, parse_mode='Markdown')

# /quote command handler
@bot.message_handler(commands=['quote'])
def send_quote(message):
    quote_msg = (
        "Here are your options for getting a Hindi quote:\n"  
        "- **Random:** Get a random Hindi quote."
    )

    # Create a custom keyboard
    markup = ReplyKeyboardMarkup(row_width=2) 
    markup.row(KeyboardButton("Random"), KeyboardButton("Test"))
    bot.send_message(message.chat.id, quote_msg, reply_markup=markup)

# Handle user responses to buttons
@bot.message_handler(func=lambda message: message.text in ["Random", "Test"])
def quote_option(message):
    if message.text == "Random":
        quote = get_quote()  # Get random quote
        bot.send_message(message.chat.id, f"Here’s your quote:\n")
        bot.send_message(message.chat.id, f"{quote}")
    elif message.text == "Test":
        bot.send_message(message.chat.id, "This is just a test response!")

    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id,text="", reply_markup=markup)

# Handle unexpected input
@bot.message_handler(func=lambda message: True)
def handle_unexpected(message):
    bot.reply_to(message, "I didn't understand that. Please use the menu options.")

# Fetch a random Hindi quote
def get_quote():
    url = "https://hindi-quotes.vercel.app/random"
    response = requests.get(url)
    
    #types- success, sad, motivational, love, attitude, positive, 
    if response.status_code == 200:
        data = response.json()  
        return data.get("quote", "Sorry, I couldn't fetch a quote right now.")
    else:
        return f"Failed to retrieve data. Status code: {response.status_code}"

bot.infinity_polling()
