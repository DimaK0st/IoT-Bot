from pprint import pprint

import telebot
from fuzzywuzzy import fuzz
from telebot import types
from Controllers.actions import execute_cmd, getFormatedLight
from constant import OPTS, KNT
from variables import currentTemp
from variables import lights, currentTemp, conditionerState, botObj, user_id, msgTemp


def callback(message):
    print("\n[log] Распознано: " + message)
    print(user_id)
    if message.startswith(OPTS["alias"]):
        cmd = message

        for x in OPTS['alias']:
            cmd = cmd.replace(x, "").strip()

        for x in OPTS['tbr']:
            cmd = cmd.replace(x, "").strip()

        cmd = recognize_cmd(cmd)
        return execute_cmd(cmd['cmd'], cmd['old'])


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0, 'old': cmd}
    for c, v in OPTS['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


class BotTg:

    def __init__(self, bot):
        global botObj

        @bot.message_handler(commands=['start'])
        def start(message):
            info = ''
            temp = 'Як можна звертатись до бота: '

            for alias in OPTS['alias']:
                print('aliasalias', alias)
                temp += ', ' + alias

            info += temp + '\n'
            temp = ''

            for ind, light in lights.items():
                temp += ', ' + light['name']

            info += """Команди які знає бот:
        ... зроби(встанови) температуру (температура),
        ... увімкни світло у %s,
        ... вимкни світло у %s,
        ... статус квартири,""" % (temp, temp)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Іван, розпочалась комендантська година')
            btn2 = types.KeyboardButton('Іван, увімкни світло у всій квартирі')
            btn3 = types.KeyboardButton('/start')
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id, info,
                             reply_markup=markup)

        @bot.message_handler(content_types=['sticker'])
        def get_text_stickers(message):
            global botObj
            botObj['user_id'] = message.from_user.id
            botObj['chat_id'] = message.chat.id
            if (message.sticker.file_unique_id):
                send = callback('Іван ' + str(KNT))

        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            global botObj
            botObj['user_id'] = message.from_user.id
            botObj['chat_id'] = message.chat.id

            send = callback(message.text)

            if send:
                global msgTemp
                msgTemp['value'] = message.text
                msg = bot.send_message(message.from_user.id,
                                       send,
                                       parse_mode='Markdown')
                botObj['msg_id'] = msg.message_id

        print('bot')
