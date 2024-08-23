from dotenv import load_dotenv
from telegrambot import bot

load_dotenv()

if __name__ == "__main__":
    bot.polling()