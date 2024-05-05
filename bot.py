import telebot
import logging
from config import *
from yandex_gpt import *
from validators import *
from database import *


logging.basicConfig(filename=LOGS, level=logging.ERROR, format='%asctime(s) FILE: %(filename)s IN: %(funcName)s '
                                                               'MESSAGE: %(message)s')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 'Привет! Отправь мне голосовое или текстовое сообщение.')


@bot.message_handler(commands=['help'])
def help(m):
    bot.send_message(m.chat.id, 'Я - бот, подключённый к нейросети компании Yandex.\n'
                                'Я умею свободно общаться с пользователем. \n'
                                'Отвечаю на текстовые сообщения текстом, на голосовые - голосом.')


@bot.message_handler(commands=['debug'])
def debug(m):
    with open('logs.txt', 'rb') as f:
        bot.send_document(m.chat.id, f)


@bot.message_handler(content_types=['voice'])
def handle_voice(m: telebot.types.Message):
    pass


@bot.message_handler(content_types=['text'])
def handle_text(m):
    try:
        user_id = m.from_user.id
        status_check_users, error_message_1 = check_number_of_users(user_id)
        if not status_check_users:
            bot.send_message(user_id, error_message_1)
            return
        full_user_message = [m.text, 'user', 0, 0, 0]
        add_message(user_id=user_id, full_message=full_user_message)
        last_messages, total_spent_tokens = select_n_last_messages(user_id, COUNT_LAST_MSG)
        total_gpt_tokens, error_message_2 = is_gpt_token_limit(last_messages, total_spent_tokens)
        if error_message_2:
            bot.send_message(user_id, error_message_2)
            return
        status_gpt, answer_gpt, tokens_in_answer = ask_gpt(last_messages)
        if not status_gpt:
            bot.send_message(user_id, answer_gpt)
            return
        total_gpt_tokens += tokens_in_answer
        full_gpt_message = [answer_gpt, 'assistant', total_gpt_tokens, 0, 0]
        add_message(user_id=user_id, full_message=full_gpt_message)
        bot.send_message(user_id, answer_gpt, reply_to_message_id=m.id)
    except Exception as e:
        logging.error(e)
        bot.send_message(m.from_user.id, 'Не получилось ответить. Попробуй написать другое сообщение.')


@bot.message_handler(func=lambda: True)
def handler(m):
    bot.send_message(m.from_user.id, 'Отправь мне голосовое или текстовое сообщение.')


bot.polling()