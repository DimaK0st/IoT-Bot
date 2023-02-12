import logging
import threading
import time
from variables import currentTemp


def thread_conditioner(temp):
    global currentTemp
    global conditionerState
    print("Кондиціонер почав працювати при температурі: %d" % currentTemp['value'])
    conditionerState = True

    if currentTemp['value'] >= temp:
        while (currentTemp['value'] > temp):
            time.sleep(5)
            currentTemp['value'] -=1
            print('Температура знизилась до: %d' % currentTemp['value'])
    else:
        while (currentTemp['value'] < temp):
            time.sleep(5)
            hui(True)
            print('Температура підвищилась до: %d' % currentTemp['value'])

    conditionerState = False
    print("Кондиціонер закінчив працювати")

def hui(bool):
    global currentTemp

    if bool:
        currentTemp['value'] = currentTemp['value']+1
    else:
        currentTemp['value'] = currentTemp['value']-1
