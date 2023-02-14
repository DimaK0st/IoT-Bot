import os
import threading
import time
import pyttsx3
import datetime
from fuzzywuzzy import fuzz

# настройки
from Controllers.actions import execute_cmd
from Controllers.threads import thread_conditioner, emulator_degrees, protection_func
from constant import GET_TEMP, SET_TEMP, TURN_ON_LIGHT, TURN_OFF_LIGHT, OPTS


def callback(message):
    print("\n[log] Распознано: " + message)

    if message.startswith(OPTS["alias"]):
        cmd = message

        for x in OPTS['alias']:
            cmd = cmd.replace(x, "").strip()

        for x in OPTS['tbr']:
            cmd = cmd.replace(x, "").strip()

        # распознаем и выполняем команду
        cmd = recognize_cmd(cmd)
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


x = threading.Thread(target=emulator_degrees, args=())
x.start()
x = threading.Thread(target=protection_func, args=())
x.start()

callback('Іван в якому стані зараз кондиціонер?')
callback('Іван яка зараз температура?')
callback('Іван які лампи зараз увімкнено')
callback('Іван увімкни світло у Кухні')
callback('Іван увімкни світло у Кімнаті')
callback('Іван які лампи зараз увімкнено')
callback('Іван зроби температуру 31')

time.sleep(9)
callback('Іван яка зараз температура?')
callback('Іван в якому стані зараз кондиціонер?')
callback('Іван увімкни світло у всій квартирі')
callback('Іван почалась комендантська година')
time.sleep(9)
callback('Іван яка зараз температура?')
callback('Іван в якому стані зараз кондиціонер?')
time.sleep(9)
callback('Іван яка зараз температура?')
callback('Іван в якому стані зараз кондиціонер?')
callback('Іван в якому стані зараз квартира?')

time.sleep(20)
