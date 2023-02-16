import logging
import threading
import time
from random import randint

from variables import currentTemp, protection
from variables import lights, currentTemp, conditionerState, botObj, user_id


def thread_conditioner(temp, prot=False):
    global conditionerState
    global currentTemp
    print("Кондиціонер почав працювати при температурі: %d" % currentTemp['value'])
    printBot("Кондиціонер почав працювати при температурі: %d" % currentTemp['value'])

    conditionerState['value'] = True
    if prot:
        protection['value'] = True

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

    protection['value']=False
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
            global protection
            conditionerState['value'] = False
            protection['value']=True
            time.sleep(6)
            x = threading.Thread(target=thread_conditioner, args=(25,True,))
            x.start()


def incOrDecTemp(bool):
    global currentTemp

    if bool:
        currentTemp['value'] = currentTemp['value'] + 1
    else:
        currentTemp['value'] = currentTemp['value'] - 1


def getFormatedLight():
    global conditionerState
    global lights
    res = '\n'

    for ind, light in lights.items():
        res += str(ind) + '-' + (' 💡', ' 🚨')[light['state']] + '-' + light['name'] + '\n'

    res += 'Кондиціонер-' + ('☑', '✅')[conditionerState['value']] + '\n'

    return res


def printBot(text):
    global botObj
    global protection
    result = 'Зараз температура у кімнаті: %d°C' % currentTemp['value']
    result += getFormatedLight()
    result += '\n' + text
    print(protection)
    if(protection['value']):
        result += '\n' + '🛑Було увімкнено екстрену зміну температури🛑'

    if botObj['bot'] == '' or botObj['user_id'] == 0:
        return

    if botObj['chat_id'] != 0 and botObj['msg_id'] != 0:
        botObj['bot'].edit_message_text(chat_id=botObj['user_id'], message_id=botObj['msg_id'],
                                        text=result, parse_mode='Markdown')
