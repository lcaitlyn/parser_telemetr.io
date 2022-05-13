from cgitb import html
from email import message
from unicodedata import name
from bs4 import PageElement
import telebot
from telebot import types
import parser
from parser import parse


token = '5356400211:AAEALKuF0Xm-fYvllYfz9r0inLWeNTJvEx4'
#token = '123567:ABCDEFD'  <- example

bot = telebot.TeleBot(token)
t_url = 'https://telemetr.io/'
URL = ""

@bot.message_handler(commands=['start'])
def start(message):
    sticker = open ('stickers/pirate.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Начать парсинг', callback_data='start'))
    mes = "Привет, <b>" + message.from_user.first_name + "</b>!\nЭто парсер телеметра 🏴‍☠️\n\n<b>Чтобы начать парсинг нажми кнопку внизу ⬇️</b>"
    bot.send_message(message.chat.id, mes, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_message(message):
    bot.send_message(message.chat.id, 'Жми /start', parse_mode='html')

def get_url(message):
    if message.text.find(t_url, 0, len(t_url)) == 0:
        start_parse(message)
    else:
        bot.send_message(message.chat.id, "<b>Неверная ссылка!</b>\n"
            + 'Она должна содержать '+ t_url + '\n'
            + 'Чтобы начать заного пиши /start', parse_mode='html')
        bot.register_next_step_handler(message, get_url)
    

def start_parse(message):
    bot.register_next_step_handler(message, get_message)
    bot.send_message(message.chat.id, '🕵️‍♂️ Парсинг начался...')
    parse(bot, message)
    

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'start':
            bot.edit_message_text(text=call.message.text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None,)
            bot.send_message(call.message.chat.id, '*Введите ссылку.*\n\nПример:\n'
                + '1) `https://telemetr.io/en/channels?subscribers=19990,20000&avg=1500,2000` (5 каналов)\n'
                + '2) `https://telemetr.io/en/channels?subscribers=18000,20000` (100 каналов)\n'
                + '_Нажми на ссылку она скопируется_', parse_mode='Markdown')
            bot.register_next_step_handler(call.message, get_url)
        

if __name__ == '__main__':
    if token == 'put your token here':
        print ('Вставьте token из @botfather!')
    else:
        bot.polling(none_stop=True, interval=0)
        bot.send_message()
    
