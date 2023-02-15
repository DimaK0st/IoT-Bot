import logging
import threading
import time
from random import randint

from variables import currentTemp
from variables import lights, currentTemp, conditionerState, botObj, user_id


def thread_conditioner(temp):
    global conditionerState
    global currentTemp
    print("Кондиціонер почав працювати при температурі: %d" % currentTemp['value'])
    printBot("Кондиціонер почав працювати при температурі: %d" % currentTemp['value'])

    conditionerState['value'] = True

    if currentTemp['value'] >= temp:
        while (currentTemp['value'] > temp):
            time.sleep(1)

            if not conditionerState['value']:
                break
            incOrDecTemp(False)
            print('Температура знизилась до: %d' % currentTemp['value'])
            printBot('Температура знизилась до: %d' % currentTemp['value'])
    else:
        while (currentTemp['value'] < temp):
            time.sleep(1)

            if not conditionerState['value']:
                break

            incOrDecTemp(True)
            print('Температура підвищилась до: %d' % currentTemp['value'])
            printBot('Температура підвищилась до: %d' % currentTemp['value'])

    conditionerState['value'] = False
    print("Кондиціонер закінчив працювати")
    printBot("Кондиціонер закінчив працювати")


def emulator_degrees():
    i = 0

    while i < 50:
        incOrDecTemp(True)
        print("Температура підвищилась на 1 градус, зараз: %d" % currentTemp['value'])
        printBot("Температура підвищилась на 1 градус, зараз: %d" % currentTemp['value'])
        time.sleep(10)
        i += 1

    while True:
        time.sleep(10)
        rand = randint(-1, 1)
        print("Температура змінилась на %d градус, зараз: %d" % (rand, currentTemp['value']))
        printBot("Температура змінилась на %d градус, зараз: %d" % (rand, currentTemp['value']))
        currentTemp['value'] += rand


def protection_func():
    x = ''
    while 0 < 2:

        if (currentTemp['value'] > 32 or currentTemp['value'] < 18) and (x == '' or not x.is_alive()):
            global conditionerState
            conditionerState['value'] = False
            time.sleep(6)
            x = threading.Thread(target=thread_conditioner, args=(25,))
            x.start()


def incOrDecTemp(bool):
    global currentTemp

    if bool:
        currentTemp['value'] = currentTemp['value'] + 1
    else:
        currentTemp['value'] = currentTemp['value'] - 1


def getFormatedLight():
    res = ''
    for ind, light in lights.items():
        res += str(ind) + (' 💡', ' 🚨')[light['state']]


def printBot(text):
    global botObj

    print('botObj111111111111', botObj)

    if botObj['bot'] == '' or botObj['user_id'] == 0:
        return

    print("botObj['chat_id']!=0 and botObj['msg_id']", botObj['chat_id'], botObj['msg_id'])

    if botObj['chat_id'] != 0 and botObj['msg_id'] != 0:
        print('editsdasdasd')
        botObj['bot'].edit_message_text(chat_id=botObj['user_id'], message_id=botObj['msg_id'],
                                        text=text, parse_mode='Markdown')
    else:
        print('text', botObj['user_id'])
        botObj['bot'].send_message(botObj['user_id'],
                                   text,
                                   parse_mode='Markdown')
