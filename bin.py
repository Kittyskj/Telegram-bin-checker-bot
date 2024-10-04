import requests 
import telebot

import emoji

bot = telebot.TeleBot("your api")

author_name = 'your name'

hrestik = emoji.emojize(":cross_mark:")
galochka = emoji.emojize(":check_mark:")

@bot.message_handler(commands=['start'])
def welcome(message):
    icon = '😁'
    welcome_msg = f'Hello, {message.from_user.first_name}! {icon}\n' \
                  f'I am a bot created by {author_name} to retrieve BIN data.\n' \
                  f'To get started, click on the command to learn more /help.'
    bot.send_message(message.from_user.id, welcome_msg)

@bot.message_handler(commands=['help'])
def helping(message):
    help_msg = f'To proceed, read the example, and then write your BIN in string format in the chat.\n' \
               f'Example BIN: 4571 7360 <-- incorrect, correct --> 45717360\n' \
               f'The bot is still in very early development, Alpha Version 1.3'
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
        
        poluchaem = perepid(prepaid)
        poluch = luhna(bin_luhn)
        site = sitebank(bank_url)
        cityx = city(bank_city)

        return f" Info: Card number length: {bin_length}\n Luhn algorithm: {poluch}\n " \
               f" Payment system scheme: {scheme_bin}\n Card type: {type_bin}\n " \
               f" Card brand: {brand}\n Prepaid: {poluchaem}\n " \
               f" Country by number: {country_numeric}\n Country abbreviation: {country_alpha2}\n Country name: {country_name}\n Country flag: {country_emoji}\n Country currency: {country_currency}\n " \
               f" Bank name: {bank_name}\n Bank website: {site}{bank_url}\n Bank phone number: {bank_phone}\n Bank city: {cityx}{bank_city}\n "
    
    return "This BIN does not exist! Please try again."

def perepid(TrueFalse):
    if str(TrueFalse) == "False":
        return hrestik
    elif str(TrueFalse) == "True":
        return galochka

def luhna(TrueFals):
    if str(TrueFals) == "False":
        return hrestik
    elif str(TrueFals) == "True":
        return galochka

def sitebank(TrueFals):
    if str(TrueFals) == "None":
        return hrestik

def city(TrueFals):
    if str(TrueFals) == "None":
        return hrestik

bot.polling(none_stop=True)
