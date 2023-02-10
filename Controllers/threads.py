import logging
import threading
import time
from variables import currentTemp


def thread_conditioner(temp):
    global currentTemp
    global conditionerState
    print("Кондиціонер почав працювати при температурі: %d" % currentTemp)
    conditionerState = True

    if currentTemp >= temp:
        while (currentTemp > temp):
            time.sleep(5)
            currentTemp = currentTemp - 1
            print('Температура знизилась до: %d' % currentTemp)
    else:
        while (currentTemp < temp):
            time.sleep(5)
            currentTemp = currentTemp + 1
            print('Температура підвищилась до: %d' % currentTemp)

    conditionerState = False
    print("Кондиціонер закінчив працювати")
