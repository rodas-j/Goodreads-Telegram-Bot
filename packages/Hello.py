'''
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#post-a-text-message
'''
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
import urllib.parse
from urllib.parse import urlparse

def googleSearch(query):
    dict_results = {}
    g_clean = [ ] #this is the list we store the search results
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query) #this is the actual query we are going to scrape
    try:
            html = requests.get(url)
            if html.status_code==200:
                soup = BeautifulSoup(html.text, 'lxml')
                a = soup.find_all('a') # a is a list
                for i in a:
                    k = i.get('href')
                    try:
                        m = re.search("(?P<url>https?://[^\s]+)", k)
                        n = m.group(0)
                        rul = n.split('&')[0]
                        domain = urlparse(rul)
                        if(re.search('google.com', domain.netloc)):
                            continue
                        else:
                            g_clean.append(rul)
                    except:
                        continue
                filtered_results = [x for x in g_clean if 'goodreads.com' in x]
                
                for i in filtered_results:
                    res = requests.get(i)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    dict_results[soup.title.getText()] = i
    except Exception as ex:
            print(str(ex))
    finally:
            return dict_results

def googleGoodreads(search): #TODO: Needs to be much faster
    results = googleSearch(search + " Goodreads")
    return results


bot = telegram.Bot(token='621697472:AAFIgz7WpxP34D_kSBeSiblYm6ZxjrpC67Q')


updater = Updater(token='621697472:AAFIgz7WpxP34D_kSBeSiblYm6ZxjrpC67Q', use_context=True)
dispatcher = updater.dispatcher #for quick access of dispatcher

x = 5
elaborate_text = f'''Invalid Input'''

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO) #Exception Handling: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Exception-Handling

def start(update, context):
    username = update.message.from_user.first_name
    text = f"Hey, {username}! \nWelcome to my fun little project. Start by typing the title of the book you're looking for"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)

def hi(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hey, man!")

def echo(update, context):
    received_message = update.message.text
    chat_id = update.effective_chat.id
    print(f'{chat_id}: {received_message}')
    reply = formatted_results(get_results(download_page(search_in_goodreads(received_message))), 10)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode=telegram.ParseMode.HTML)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def book(update, context):
    link = update.message.text.replace('/bk_', 'https://www.goodreads.com/book/show/')
    print(link)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

start_handler = CommandHandler('start', start)
hi_handler = CommandHandler('hi', hi)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(hi_handler)
try:
    dispatcher.add_handler(MessageHandler(Filters.regex('^(/bk_[\d]+)$'), book))
except:
    print("error")
    updater.stop()
updater.start_polling()

'''
The Filters class contains a number of functions that filter incoming messages for text,
 images, status updates and more. Any message that returns True for at least one of the
 filters passed to MessageHandler will be accepted. You can also write your own filters 
 if you want.
 '''

 
