import logging
import math
from config import *
from database import *
from yandex_gpt import *

logging.basicConfig(filename=LOGS, level=logging.ERROR, format='%(asctime)s FILE: %(filename)s IN: %(funcName)s '
                                                               'MESSAGE: %(message)s', filemode='w')


def check_number_of_users(user_id):
    count = count_users(user_id)
    if count is None:
        return None, 'Ошибка при работе с БД'
    if count > MAX_USERS:
        return None, 'Превышено максимальное количество пользователей'
    return True, ''


def is_gpt_token_limit(message, total_spent_tokens):
    all_tokens = count_gpt_tokens(message) + total_spent_tokens
    if all_tokens > MAX_USER_GPT_TOKENS:
        return None, f'Превышен максимальный лимит токенов {MAX_USER_GPT_TOKENS}'
    return all_tokens, ''


def is_stt_block_limit(user_id, duration):
    # TODO:
    pass


def is_tts_symbol_limit(user_id, text):
    # TODO:
    pass
