import os
import telebot
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('BOT_TOKEN') 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(telebot.types.KeyboardButton('🟢 Текущий онлайн'), telebot.types.KeyboardButton('❗️ Голосовать'))
    markup.add(telebot.types.KeyboardButton('🐱 Котики'), telebot.types.KeyboardButton('🐶 Собакены'))

    bot.send_message(message.chat.id, 'Привет! Я бот проекта Syndicate. Выбери одну из кнопок:', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def get_info(message):
    if message.text == '🟢 Текущий онлайн':
        url = 'https://api.wargm.ru/v1/server/info?client=60685:jz_ymGQ_B6J_e7g1J_Rl73DiWB5gCKd6'
        response = requests.get(url).json()
        online_players = response['responce']['data']['players']
        max_players = response['responce']['data']['players_max']
        bot.send_message(message.chat.id, f'Текущий онлайн: {online_players} из {max_players}')
    elif message.text == '❗️ Голосовать':
        bot.send_message(message.chat.id, 'Голосование за сервер: https://wargm.ru/server/60685/votes')
    elif message.text == '🐱 Котики':
        url = 'https://api.thecatapi.com/v1/images/search'
        response = requests.get(url).json()
        cat_url = response[0]['url']
        bot.send_photo(message.chat.id, cat_url)
    elif message.text == '🐶 Собакены':
        url = 'https://dog.ceo/api/breeds/image/random'
        response = requests.get(url).json()
        dog_url = response['message']
        bot.send_photo(message.chat.id, dog_url)

bot.polling()