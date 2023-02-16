import telebot
from fuzzywuzzy import fuzz
from telebot import types

from Controllers.actions import execute_cmd, getFormatedLight
from constant import OPTS

from variables import currentTemp
from variables import lights, currentTemp, conditionerState, botObj, user_id


def callback(message):
    print("\n[log] Распознано: " + message)
    print(user_id)
    if message.startswith(OPTS["alias"]):
        cmd = message

        for x in OPTS['alias']:
            cmd = cmd.replace(x, "").strip()

        for x in OPTS['tbr']:
            cmd = cmd.replace(x, "").strip()

        # распознаем и выполняем команду
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
        print('botObj', botObj)

        @bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Допомога")
            markup.add(btn1)
            bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)

        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):

            global botObj
            botObj['user_id'] = message.from_user.id
            botObj['chat_id'] = message.chat.id

            send = callback(message.text)
            print('////////////////////////////////', send)
            print('send',send)
            if send:
                print("*************************", send)
                msg = bot.send_message(message.from_user.id,
                                       send,
                                       parse_mode='Markdown')
                print("------------------------------------------------------", msg)
                botObj['msg_id'] = msg.message_id
            print('hui')
            print('message.text',message.text)

            if message.text == 'Допомога':
                info = ''
                temp ='Як можна звертатись до бота: '
                print("OPTS['alias'].items()",OPTS['alias'])
                for alias in OPTS['alias']:
                    print('aliasalias',alias)
                    temp += ', ' + alias
                info += temp + '\n'
                temp = ''
                for ind, light in lights.items():
                    print('lightlightlight',light)
                    temp += ', ' + light['name']
                print(info)
                info += """Команди які знає бот:
... зроби(встанови) температуру (температура),
... увімкни світло у %s,
... вимкни світло у %s,
... статус квартири,""" % (temp,temp)
                print(info)

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
                btn1 = types.KeyboardButton('Іван, розпочалась комендантська година')
                btn2 = types.KeyboardButton('Іван, увімкни світло у всій квартирі')
                btn3 = types.KeyboardButton('Допомога')
                markup.add(btn1, btn2, btn3)
                bot.send_message(message.from_user.id, info,
                                 reply_markup=markup)  # ответ бота


            elif message.text == 'Как стать автором на Хабре?':
                bot.send_message(message.from_user.id,
                                 'Вы пишете первый пост, его проверяют модераторы, и, если всё хорошо, отправляют в основную ленту Хабра, где он набирает просмотры, комментарии и рейтинг. В дальнейшем премодерация уже не понадобится. Если с постом что-то не так, вас попросят его доработать.\n \nПолный текст можно прочитать по ' + '[ссылке](https://habr.com/ru/sandbox/start/)',
                                 parse_mode='Markdown')

            elif message.text == 'Правила сайта':
                bot.send_message(message.from_user.id,
                                 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/docs/help/rules/)',
                                 parse_mode='Markdown')

            elif message.text == 'Советы по оформлению публикации':
                bot.send_message(message.from_user.id,
                                 'Подробно про советы по оформлению публикаций прочитать по ' + '[ссылке](https://habr.com/ru/docs/companies/design/)',
                                 parse_mode='Markdown')

        print('bot')
