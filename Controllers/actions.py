import datetime
import os
import re
import threading
from pprint import pprint

from fuzzywuzzy import fuzz

from Controllers.threads import thread_conditioner
from constant import GET_TEMP, SET_TEMP, TURN_ON_LIGHT, TURN_OFF_LIGHT, OPTS, GET_LIGHT
from variables import lights, currentTemp

def execute_cmd(cmd, old):
    if cmd == GET_TEMP:
        global currentTemp
        print("Зараз температура: %d °C" % currentTemp['value'])

    elif cmd == SET_TEMP:

        for x in OPTS['cmds'][SET_TEMP]:
            old = old.replace(x, "").strip()

        degrees = re.findall('[0-9]+', old)[0]

        x = threading.Thread(target=thread_conditioner, args=(int(degrees),))
        x.start()

    elif cmd == TURN_ON_LIGHT:
        lightManager(TURN_ON_LIGHT, True, old)
        print('Світло було увімкнено у ' + old)


    elif cmd == TURN_OFF_LIGHT:
        lightManager(TURN_OFF_LIGHT, False, old)
        print('Світло було вимкнено у ' + old)

    elif cmd == GET_LIGHT:

        pprint(lights)

    else:
        print('Команда не розпізнана, будь ласка повторіть спробу!')


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