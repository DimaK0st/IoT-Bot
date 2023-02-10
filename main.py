import os
import threading
import time
import pyttsx3
import datetime
from fuzzywuzzy import fuzz

# настройки
from Controllers.actions import execute_cmd
from Controllers.threads import thread_conditioner
from constant import GET_TEMP, SET_TEMP, TURN_ON_LIGHT, TURN_OFF_LIGHT, OPTS

def callback(message):
    print("[log] Распознано: " + message)

    if message.startswith(OPTS["alias"]):
        # обращаются к Кеше
        cmd = message

        for x in OPTS['alias']:
            cmd = cmd.replace(x, "").strip()

        for x in OPTS['tbr']:
            cmd = cmd.replace(x, "").strip()

        # распознаем и выполняем команду
        cmd = recognize_cmd(cmd)
        # print('cmd')
        # print(cmd)
        execute_cmd(cmd['cmd'], cmd['old'])


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0, 'old': cmd}
    for c, v in OPTS['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


callback('Іван яка зараз температура 34')
callback('Іван увімкни світло у Кухні')
callback('Іван увімкни світло у Кімнаті')
callback('Іван які лампи зараз увімкнено')
callback('Іван зроби температуру 31')


time.sleep(20)