import telebot
import config
from use_db import make_user

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_dialog(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    organization_button = telebot.types.KeyboardButton('Организация')
    user_button = telebot.types.KeyboardButton('Личное пользование')
    markup.add(organization_button, user_button)

    make_user(message.chat.id, message.from_user.username)

    bot.send_message(message.chat.id,
                     'Привет, я телеграм-бот Имя, который проверяет различные материалы на наличие их в регистре экстремистских материалов МЮ РФ')
    bot.send_message(message.chat.id,
                     'Если вы собираетесь использовать для отслеживания запрещённых книг в своей библиотеке, то нажмите Организация, иначе нажмите Личное пользование ',
                     reply_markup=markup)


def find_material(message):
    bot.send_message(message.chat.id, message.text)
    # запрос


def check_material(message):
    bot.send_message(message.chat.id, "Отправьте файл(список)")
    # запрос


def report_material(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['find'])
def find_handler(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['check'])
def check_handler(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['report'])
def report_handler(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=["text"])
def bar(message):
    if message.text == "Организация":
        type = "organization"
        organization_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        find_button = telebot.types.KeyboardButton("Проверка материала на наличие в реестре запрещённых материалов")
        check_button = telebot.types.KeyboardButton("Проверка списка материалов в реестре на наличие запрещённой литературы")
        make_act_button = telebot.types.KeyboardButton("Составление акта")

        organization_markup.add(find_button, check_button, make_act_button)
        bot.send_message(message.chat.id,
                         "Список команд:\n1)Проверка материала на наличие в реестре запрещённых материалов - /find [name]\n2)"
                         "Проверка списка материалов в реестре на наличие запрещённой литературы - /check"
                         "\n3)Составление акта",
                         reply_markup=organization_markup)
    elif message.text == "Личное пользование":
        type = "person"
        person_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        find_button = telebot.types.KeyboardButton("Проверка материала на наличие в реестре запрещённых материалов")
        report_button = telebot.types.KeyboardButton("Отправить жалобу на материал")
        person_markup.add(find_button, report_button)
        bot.send_message(message.chat.id,
                         "Список команд:\n1)Проверка материала на наличие в реестре запрещённых материалов - /find [name]\n2)Отправить жалобу на материал - /report [name]",
                         reply_markup=person_markup)
    elif message.text == "Проверка материала на наличие в реестре запрещённых материалов":
        bot.send_message(message.chat.id, "Отправьте название")
        bot.register_next_step_handler(message, find_material)
    elif message.text == "Проверка списка материалов в реестре на наличие запрещённой литературы":
        bot.send_message(message.chat.id, "Отправьте название")
        bot.register_next_step_handler(message, check_material)
    elif message.text == "Отправить жалобу на материал":
        bot.send_message(message.chat.id, "Отправьте название")
        bot.register_next_step_handler(message, report_material)
    elif message.text == "2)Отправить жалобу на материал":
        bot.send_message(message.chat.id, "Опишите свою проблему")
        #берёт описание проблемы
        bot.register_next_step_handler(message, report_material)
    else:
        bot.send_message(message.chat.id,"Непонятная команда /help")

bot.polling(none_stop=True)
