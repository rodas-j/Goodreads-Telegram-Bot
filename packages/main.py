from telegram.ext import Updater
import logging  #for debugging purposes
from telegram.ext import CommandHandler 
from telegram.ext import RegexHandler 
from telegram.ext import MessageHandler, Filters
import telegram
import requests
from bs4 import BeautifulSoup
import re
from Goodreads_Search import *
from Goodreads_Page import *
import urllib.parse
from urllib.parse import urlparse

bot = telegram.Bot(token='621697472:AAFIgz7WpxP34D_kSBeSiblYm6ZxjrpC67Q')

updater = Updater(token='621697472:AAFIgz7WpxP34D_kSBeSiblYm6ZxjrpC67Q', use_context=True)
dispatcher = updater.dispatcher #for quick access of dispatcher

#Exception Handling: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Exception-Handling
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO) 

def start(update, context):
    username = update.message.from_user.first_name
    exec(f"""def {username.lower()}(text):return print(text)""")
    text = f"Hey, {username}! \nWelcome to my fun little project. Start by typing the title of the book you're looking for"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)

def search(update, context):
    received_message = update.message.text
    print(f'{update.message.from_user.first_name}: {received_message}')
    results = formatted_results(get_results(download_page(search_in_goodreads(received_message))), 10)
    context.bot.send_message(chat_id=update.effective_chat.id, text=results, parse_mode=telegram.ParseMode.HTML)

def book_command(update, context):
    chat_id = update.effective_chat.id
    link = update.message.text.replace('/bk_', 'https://www.goodreads.com/book/show/')
    book = Book()
    text = book.get_content(download_page(link)).format_result()
    image_link = book.image
    context.bot.send_photo(chat_id=chat_id, photo=image_link, caption=text, parse_mode=telegram.ParseMode.HTML)

def main():
    search_handler = MessageHandler(Filters.text & (~Filters.command), search)
    dispatcher.add_handler(search_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    book_command_handler = MessageHandler(Filters.regex('^(/bk_[\d]+)$'), book_command)
    dispatcher.add_handler(book_command_handler)

    updater.start_polling()

if __name__ == "__main__":
    #https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/ 
    main()