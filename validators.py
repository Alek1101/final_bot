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
    audio_blocks = math.ceil(duration / 15)
    all_blocks = count_all_limits(user_id, 'stt_blocks') + audio_blocks
    if duration >= 30:
        return None, 'SpeechKit STT работает с голосовыми сообщениями меньше 30 секунд'
    if all_blocks >= MAX_USER_STT_BLOCKS:
        return None, (f'Превышен общий лимит SpeechKit STT {MAX_USER_STT_BLOCKS}. Использовано {all_blocks} '
                      f'доступных блоков. Доступно: {MAX_USER_STT_BLOCKS - all_blocks}')
    return audio_blocks, None


def is_tts_symbol_limit(user_id, text):
    text_symbols = len(text)
    all_symbols = count_all_limits(user_id, 'tts_symbols')
    if all_symbols >= MAX_USER_TTS_SYMBOLS:
        return None, f'Превышен общий лимит SpeechKit TTS {MAX_USER_TTS_SYMBOLS}. Использовано: {all_symbols} символов. Доступно: {MAX_USER_TTS_SYMBOLS - all_symbols}'
    if text_symbols >= 200:
        return None, f'Превышен лимит на запрос 200, в сообщении {text_symbols} символов'
    return len(text), None
