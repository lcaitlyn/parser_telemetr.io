from cmath import inf
from distutils.log import info
from operator import imod, truediv
from tkinter.messagebox import YES
from turtle import ht
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import time


'''
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='btn-light')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
'''

def get_html(url, params=None):
    r = requests.get(url, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item-list')
    channels = []
    for item in items:
        if item.find('a', class_='link text-weight username-short short-string title-hover-color'):
            info = item.find('a', class_='link text-weight username-short short-string title-hover-color')
            info2 = item.find_all('div', class_='cell item-font align-top')
            if info.find('span', class_='username'):
                link = 't.me/' + info.get('href').partition('-')[2]
            else:
                link = 't.me/joinchat/' + info.get('href').partition('-')[2]
            channels.append({
                'title': info.get('title'),
                'link': link,
                'photo': 'https://telemetr.io'.join(item.find('img', class_='circle-img').get('src')),
                'subscribers': info2[0].find('span', attrs={'itemprop': 'potentialAction'}).get_text(strip=True).partition('-')[0].partition('+')[0],
                'eyes': info2[2].find('span', attrs={'itemprop': 'potentialAction'}).get_text(strip=True).replace('~', '')
            })
    return channels
    


def print_channels(channels, bot, message):
    bot.send_message(message.chat.id, ('Найдено: ' + str(len(channels)) + ' каналов'))
    for channel in channels:
        #mes = f'✏️ Название канала: <b>' + channel['title'] + '</b>\n🔗 Ссылка: <b>' + channel['link'] + '</b>\n🙎‍♂️ Подписчиков: <b>' + channel['subscribers'] + '</b>\n👀 Просмотров: <b>' + channel['eyes'] + '</b>'
        mes = f'[Ссылка 🔗](' + channel['link'] + ') - ' + channel['subscribers'] + '🙎‍♂️ - ' + channel['eyes'] + '👀 - ' + channel['title']
        #bot.send_photo(message.chat.id, channel['photo'], mes, parse_mode='htmml')
        
        try:
            bot.send_message(message.chat.id, mes, parse_mode='markdown', disable_web_page_preview=True)
        except:
            bot.send_message(message.chat.id, 'Ошибка вывода 😕')
        time.sleep(1)
        

    
''' parse old
def parse(bot, message):
    URL = message.text
    html = get_html(URL)
    if html.status_code == 200:
        channels = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            bot.send_message(message.chat.id, '🔎 Парсинг страницы ' + str(page) + '/' + str(pages_count))
            html = get_html(URL, params={'page': page})
            channels.extend(get_content(html.text))
        print_channels(channels, bot, message)
        bot.send_message(message.chat.id, '📊 Парсинг успешно завершен.\nСпаршено <b>' + str(len(channels)) + '</b> каналов', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Ошибка: не удалось установить соединение с сайтом ❌')
'''

def parse(bot, message):
    html = get_html(message.text)
    if html.status_code == 200:
        channels = get_content(html.text)
        print_channels(channels, bot, message)
        bot.send_message(message.chat.id, '📊 Парсинг успешно завершен.', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Ошибка: не удалось установить соединение с сайтом ❌')