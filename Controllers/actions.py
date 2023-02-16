import datetime
import os
import re
import threading
from pprint import pprint
from fuzzywuzzy import fuzz
from Controllers.threads import thread_conditioner, printBot
from constant import GET_TEMP, SET_TEMP, TURN_ON_LIGHT, TURN_OFF_LIGHT, OPTS, GET_LIGHT, TURN_ON_ALL_LIGHT, \
    TURN_OFF_ALL_LIGHT, CONDITIONER_STATE, HOME_STATE
from variables import lights, currentTemp, conditionerState, botObj


def execute_cmd(cmd, old):
    global conditionerState
    if cmd == GET_TEMP:
        global currentTemp
        print("Зараз температура: %d °C" % currentTemp['value'])
        return ("Зараз температура: %d °C" % currentTemp['value'])

    elif cmd == SET_TEMP:
        global botObj
        print('bot', botObj)
        for x in OPTS['cmds'][SET_TEMP]:
            old = old.replace(x, "").strip()

        degrees = re.findall('[0-9]+', old)[0]

        x = threading.Thread(target=thread_conditioner, args=(int(degrees),))
        x.start()
        return 'Запуск процесу'

    elif cmd == TURN_ON_LIGHT:
        for x in OPTS['cmds'][TURN_ON_LIGHT]:
            old = old.replace(x, "").strip()

        lightManager(TURN_ON_LIGHT, True, old)
        return ('Світло було увімкнено у ' + old)


    elif cmd == TURN_OFF_LIGHT:
        for x in OPTS['cmds'][TURN_OFF_LIGHT]:
            old = old.replace(x, "").strip()

        lightManager(TURN_OFF_LIGHT, False, old)
        return ('Світло було вимкнено у ' + old)

    elif cmd == GET_LIGHT:
        pprint(lights)

    elif cmd == TURN_ON_ALL_LIGHT:
        for i, light in lights.items():
            light['state'] = True
        return ('Світло було увімкнено у всій квартирі')

    elif cmd == TURN_OFF_ALL_LIGHT:
        for i, light in lights.items():
            light['state'] = False
        return ('Світло було вимкнено у всій квартирі')

    elif cmd == CONDITIONER_STATE:
        global conditionerState
        return ('Кондиціонер зараз ' + ('вимкнений', 'вімкнено')[conditionerState['value']])

    elif cmd == HOME_STATE:
        return ('Обробка')


    else:
        print('Команда не розпізнана, будь ласка повторіть спробу!')
        return ('Команда не розпізнана, будь ласка повторіть спробу!')


def checkAlias(cmd):
    RC = {'cmd': '', 'percent': 0, 'old': cmd}
    for c, v in lights.items():

        for x in v['alias']:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC['cmd']


def lightManager(type, bool, str):
    global lights

    for x in OPTS['cmds'][type]:
        str = str.replace(x, "").strip()

    lights[checkAlias(str)]['state'] = bool
    return bool


def getFormatedLight():
    global conditionerState
    global lights
    res = '\n'

    for ind, light in lights.items():
        res += str(ind) + '-' + (' 💡', ' 🚨')[light['state']] + '-' + light['name'] + '\n'

    res += 'Кондиціонер-' + ('☑', '✅')[conditionerState['value']] + '\n'

    return res
