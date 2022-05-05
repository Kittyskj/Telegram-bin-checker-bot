import requests
import telebot

bot = telebot.TeleBot("your api")
author_name = 'yout name'


@bot.message_handler(commands=['start'])
def welcome(message):
    icon = '😁'
    welcome_msg = f'Привіт, {message.from_user.first_name}! {icon}\n' \
                  f'Я бот, створений {author_name} для отримання данних по бінам.\n' \
                  f'Щоб розпочати, натисни на комманду для ознайомленя /help.'
    bot.send_message(message.from_user.id, welcome_msg)


@bot.message_handler(commands=['help'])
def helping(message):
    help_msg = f'Щоб працювати далі прочитай приклад,а потім напиши в чат свій бін в строковому типі.\n' \
               f'Приклад біну:4571 7360 <-- неправильний, правильний --> 45717360\n' \
               f'Бот в дуже дуже ранній разробці, Альфа Версія 1.3'
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
        my_json = r.json()
        bin_length = my_json.get('number').get('length')
        bin_luhn = my_json.get('number').get('luhn')
        scheme_bin = my_json.get('scheme')
        type_bin = my_json.get('type')
        brand = my_json.get('brand')
        prepaid = my_json.get('prepaid')
        country_numeric = my_json.get('country').get('numeric')
        country_alpha2 = my_json.get('country').get('alpha2')
        country_name = my_json.get('country').get('name')
        country_emoji = my_json.get('country').get('emoji')
        country_currency = my_json.get('country').get('currency')
        bank_name = my_json.get('bank').get('name')
        bank_url = my_json.get('bank').get('url')
        bank_phone = my_json.get('bank').get('phone')
        bank_city = my_json.get('bank').get('city')
        return f" Інфо: Довжина номеру карти: {bin_length}\n Алогритм луна: {bin_luhn}\n " \
               f" Схема платіжної системи: {scheme_bin}\n Тип карти: {type_bin}\n " \
               f" Бренд картки: {brand}\n Передоплата: {prepaid}\n " \
               f" Країна за номером: {country_numeric}\n Абревіатура Країни: {country_alpha2}\n Назва Країни: {country_name}\n Прапор Країни: {country_emoji}\n Валюта країни: {country_currency}\n " \
               f" Назва Банку: {bank_name}\n Сайт банку: {bank_url}\n Номер телефона банка: {bank_phone}\n Місто банка: {bank_city}\n "
    return "Такого біна не існує! Спробуйте ще раз"


bot.polling(none_stop=True)
