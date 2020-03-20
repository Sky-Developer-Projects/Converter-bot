import telebot
import requests
import json


token = '1035529961:AAGzElhYYBm7aeirPsgwuyv9djwc9VQg0QQ'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    if message.text == '/start':
        bot.forward_message(chat_id=-391611419,
                            from_chat_id=message.chat.id,
                            message_id=message.message_id)
        bot.send_message(message.chat.id, 'Привет! Я бот, который конвертирует валюты. '
                                          'Напиши /help, чтобы узнать, как я работаю')
    if message.text == '/help':
        bot.forward_message(chat_id=-391611419,
                            from_chat_id=message.chat.id,
                            message_id=message.message_id)
        bot.send_message(message.chat.id,
                         '''
Соблюдай правильный синтаксис: rub usd 500. Так ты даешь мне понять, что ты хочешь преобразовать рубли в доллары.
Также не забудь, что разделителем команды (rub-usd) и суммы (500) является ПРОБЕЛ. К тому же между валютами (rub и usd) может быть любой знак. Главное один!
    
Поддерживаемые валюты:
USD - Американский доллар
RUB - Российский рубль
UAH - Украинская гривна
PLN - Польский злотый
CNY - Китайский юань
AED - Дирхам
ARS - Аргентинской песо
AUD - Австралийский доллар
BGN - Болгарский лева
BRL - Бразильский реал
BSD - Багамский доллар
                         ''')


@bot.message_handler(content_types=['text'])
def convertation(message):
    text = message.text.upper()
    bot.forward_message(chat_id=-391611419,
                        from_chat_id=message.chat.id,
                        message_id=message.message_id)

    convert1 = text[:3]
    convert2 = text[4:7]
    summa = text[8:]

    try:
        url = f'https://api.exchangerate-api.com/v4/latest/{convert1}'
        valute = requests.get(url).json()

        try:

            try:
                s = int(summa) * valute['rates'][convert2]
                bot.send_message(message.chat.id, str(summa) + ' ' + convert1 + ' = ' + str(s) + ' ' + convert2)

            except KeyError:
                bot.send_message(message.chat.id, 'Неверный формат. Проверь: все ли ты правильно написал.')

        except ValueError:
            bot.send_message(message.chat.id, 'Неверный формат. Проверь: все ли ты правильно написал.')

    except json.decoder.JSONDecodeError:
        bot.send_message(message.chat.id, 'Произошла ошибка. Возможно неправильный синтаксис. Или поробуй позже)')


bot.polling(none_stop=True, interval=0)
