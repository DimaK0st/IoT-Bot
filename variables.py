import telebot

currentTemp = {'value': 26}
excel = {'wb': ''}
user_id = 0
msgTemp = {'value': ''}
botObj = {
    'bot': '',
    'user_id': 0,
    'chat_id': 0,
    'msg_id': 0,
}
protection = {'value':False}
conditionerState = {'value': False}

lights = {
    1: {
        'name': 'Кімната',
        'alias': ('Кімната', 'Кімнаті',),
        'state': False,
    },
    2: {
        'name': 'Вітальня',
        'alias': ('Вітальня', 'Вітальні',),
        'state': False,
    },
    3: {
        'name': 'Спальня',
        'alias': ('Спальня', 'Спальні',),
        'state': False,
    },
    4: {
        'name': 'Кухня',
        'alias': ('Кухня', 'Кухні',),
        'state': False,
    },
    5: {
        'name': 'Вбиральня',
        'alias': ('Вбиральня', 'Вбиральні',),
        'state': False,
    },
    6: {
        'name': 'Зала',
        'alias': ('Зала', 'Залі',),
        'state': False,
    },
}
