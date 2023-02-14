import logging
import threading
import time
from random import randint

from variables import currentTemp
from variables import lights, currentTemp, conditionerState


def thread_conditioner(temp):
    global conditionerState
    global currentTemp
    print("Кондиціонер почав працювати при температурі: %d" % currentTemp['value'])

    conditionerState['value'] = True

    if currentTemp['value'] >= temp:
        while (currentTemp['value'] > temp):
            time.sleep(5)

            if not conditionerState['value']:
                break
            incOrDecTemp(False)
            print('Температура знизилась до: %d' % currentTemp['value'])
    else:
        while (currentTemp['value'] < temp):
            time.sleep(5)

            if not conditionerState['value']:
                break

            incOrDecTemp(True)
            print('Температура підвищилась до: %d' % currentTemp['value'])

    conditionerState['value'] = False
    print("Кондиціонер закінчив працювати")


def emulator_degrees():
    i = 0

    while i < 50:
        incOrDecTemp(True)
        print("Температура підвищилась на 1 градус, зараз: %d" % currentTemp['value'])
        time.sleep(1)
        i += 1

    while True:
        time.sleep(10)
        rand = randint(-1, 1)
        print("Температура змінилась на %d градус, зараз: %d" % (rand, currentTemp['value']))
        currentTemp['value'] += rand


def protection_func():
    x = ''
    while 0 < 2:

        if (currentTemp['value'] > 32 or currentTemp['value'] < 18) and x == '':
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
