import telebot
from extensions import APIException, CurrencyConvert
from config import TOKEN, currency

bot = telebot.TeleBot(TOKEN)


# команды бота
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f'Формат ввода: /price <имя валюты> \
<имя валюты в которую хотите перевести> \
<количество перводимой валюты>\n Пример: /price bitcoin евро 10\
Для получения списка доступных валют, введите: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def currency_names(message: telebot.types.Message):
    txt = 'Список валют:'
    for name, forename in currency.items():
        txt = '\n'.join((txt, f'{name} ({forename})'))
    bot.reply_to(message, txt)


@bot.message_handler(commands=['price'])
def get_price(message: telebot.types.Message):
    try:
        msg = message.text.split()

        if len(msg) > 4:
            raise APIException('Больше 3 параметров!')
        elif len(msg) < 4:
            raise APIException('Меньше 3 параметров!')
        
        base, qoute, amount = msg[1], msg[2], msg[3]
        base_price = CurrencyConvert.get_price(base, qoute, amount)
    except APIException as exc:
        bot.reply_to(message, f'Ошибка со стороны пользователя: \n{exc}')
    except Exception as exc:
        bot.reply_to(message, f'Приложение не отвечает. \n{exc}')
    else:
        txt = f'<{amount} {base}> в <{qoute}> - {base_price * float(amount)}'
        bot.reply_to(message, txt)


bot.polling()
