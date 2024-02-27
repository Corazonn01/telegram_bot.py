
import os
from dotenv import load_dotenv
import telebot

load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv('API_KEY')  // here we have to create an .env file with the api of the telegram channel ( you can see that in that BotFather in telegram 
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["Greet"])
def greet(message):
    bot.reply_to(message, "Hey, how is it going?")


bot.polling()
