import requests
from config import *
from creds import get_creds
IAM_TOKEN, FOLDER_ID = get_creds()


def speech_to_text(data):
    iam_token = IAM_TOKEN
    folder_id = FOLDER_ID
    params = '&'.join([
        'topic=general',
        f'folderId={folder_id}',
        'lang=ru-RU'
    ])
    headers = {
        'Authorization': f'Bearer {iam_token}',
    }
    response = requests.post(
        f'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}',
        headers=headers,
        data=data
    )
    decoded_data = response.json()
    if decoded_data.get('error_code') is None:
        return True, decoded_data.get('result')
    else:
        return False, 'При запросе в SpeechKit возникла ошибка'


def text_to_speech(text: str):
    # Токен, Folder_id для доступа к Yandex SpeechKit
    iam_token = IAM_TOKEN
    folder_id = FOLDER_ID

    # Аутентификация через IAM-токен
    headers = {
        'Authorization': f'Bearer {iam_token}',
    }
    data = {
        'text': text,  # текст, который нужно преобразовать в голосовое сообщение
        'lang': 'ru-RU',  # язык текста - русский
        'voice': 'filipp',  # голос Филиппа
        'folderId': folder_id
    }
    # Выполняем запрос
    response = requests.post('https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize', headers=headers, data=data)

    if response.status_code == 200:
        return True, response.content  # Возвращаем голосовое сообщение
    else:
        return False, "При запросе в SpeechKit возникла ошибка"
