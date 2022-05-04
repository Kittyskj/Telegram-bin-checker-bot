import requests
import telebot

bot = telebot.TeleBot("yor api")
author_name = 'your name'


@bot.message_handler(commands=['start'])
def welcome(message):
    icon = '😁'
    welcome_msg = f'Привіт, {message.from_user.first_name}! {icon}\n' \
                  f'Я бот, створений {author_name} для отримання бінів.\n' \
                  f'Щоб розпочати, натисни на комманду для ознайомленя /help.'
    bot.send_message(message.from_user.id, welcome_msg)


@bot.message_handler(commands=['help'])
def helping(message):
    help_msg = f'Щоб працювати далі прочитай приклад,а потім напиши в чат свій бін в строковому типі.\n' \
               f'Приклад біну:4571 7360 <-- неправильний, правильний --> 45717360\n' \
               f'Бот в дуже дуже ранній разробці, Альфа Версія 1.0'
    bot.send_message(message.from_user.id, help_msg)


@bot.message_handler(content_types='text')
def home(message):
    bin = message.text
    answer = get_bin(bin)
    bot.reply_to(message, answer)


def get_bin(bin):
    url = ("https://lookup.binlist.net/" + bin)

    r = requests.get(url=url)
    if r.status_code == 200:
        bin_name = r.text
        return f'Інформація по карті: {bin_name}'
    return "Такого біна не існує! Спробуйте ще раз"


bot.polling(none_stop=True)

