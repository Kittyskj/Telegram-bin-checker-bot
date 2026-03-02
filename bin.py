import requests
import telebot
import emoji

bot = telebot.TeleBot("YOUR_BOT_TOKEN_HERE")

author_name = 'YOUR_NAME_HERE'
hrestik = emoji.emojize(":cross_mark:")
galochka = emoji.emojize(":check_mark:")

def format_boolean(value):
    if value is True:
        return galochka
    elif value is False:
        return hrestik
    return f"{hrestik} None"

def format_text(value):
    if not value or str(value).lower() == "none":
        return f"{hrestik} None"
    return value

@bot.message_handler(commands=['start'])
def welcome(message):
    icon = '😁'
    welcome_msg = (f'Hello, {message.from_user.first_name}! {icon}\n'
                   f'I am a bot created by {author_name} to retrieve BIN data.\n'
                   f'To get started, click on the command to learn more /help.')
    bot.send_message(message.from_user.id, welcome_msg)

@bot.message_handler(commands=['help'])
def helping(message):
    help_msg = (f'To proceed, read the example, and then write your BIN in string format in the chat.\n'
                f'Example BIN: 4571 7360 <-- incorrect, correct --> 45717360\n'
                f'The bot is still in very early development, Alpha Version 1.3')
    bot.send_message(message.from_user.id, help_msg)

@bot.message_handler(content_types=['text'])
def home(message):
    raw_text = message.text.strip().replace(" ", "").replace("-", "")
    if len(raw_text) < 6 or not raw_text.isdigit():
        bot.reply_to(message, "❌ Please enter a valid BIN (6-8 digits) or card number.")
        return
    
    bin_number = raw_text[:8]
    answer = get_bin(bin_number)
    bot.reply_to(message, answer)

def get_bin(bin_number):
    url = "https://lookup.binlist.net/" + bin_number
    headers = {'Accept-Version': '3'}
    try:
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            my_json = r.json()
            num_inf = my_json.get('number', {})
            cnt_inf = my_json.get('country', {})
            bnk_inf = my_json.get('bank', {})

            res = (
                f" Info:\n"
                f" Card number length: {format_text(num_inf.get('length'))}\n"
                f" Luhn algorithm: {format_boolean(num_inf.get('luhn'))}\n"
                f" Payment system scheme: {format_text(my_json.get('scheme'))}\n"
                f" Card type: {format_text(my_json.get('type'))}\n"
                f" Card brand: {format_text(my_json.get('brand'))}\n"
                f" Prepaid: {format_boolean(my_json.get('prepaid'))}\n"
                f" Country by number: {format_text(cnt_inf.get('numeric'))}\n"
                f" Country abbreviation: {format_text(cnt_inf.get('alpha2'))}\n"
                f" Country name: {format_text(cnt_inf.get('name'))}\n"
                f" Country flag: {cnt_inf.get('emoji', '')}\n"
                f" Country currency: {format_text(cnt_inf.get('currency'))}\n"
                f" Bank name: {format_text(bnk_inf.get('name'))}\n"
                f" Bank website: {format_text(bnk_inf.get('url'))}\n"
                f" Bank phone number: {format_text(bnk_inf.get('phone'))}\n"
                f" Bank city: {format_text(bnk_inf.get('city'))}"
            )
            return res
        elif r.status_code == 404:
            return "This BIN does not exist! Please try again."
        elif r.status_code == 429:
            return "Too many requests. Try again later."
        else:
            return f"Error: Status code {r.status_code}"
    except:
        return "An error occurred."

bot.polling(none_stop=True)
