GET_TEMP = 1
SET_TEMP = 2

TURN_ON_LIGHT = 3
TURN_OFF_LIGHT = 4

TURN_ON_ALL_LIGHT = 5
TURN_OFF_ALL_LIGHT = 6

GET_LIGHT = 7
CONDITIONER_STATE = 8
HOME_STATE = 9
PATRIOT = 10
KNT = 11
SAVE = 12

OPTS = {
    "alias": ('Іван', 'Бот', 'Товариш', 'Приятель', 'Побратим'),
    "tbr": ('скажи', 'як', 'яка'),
    "cmds": {
        GET_TEMP: ('яка зараз температура', 'яка температура', 'температура в кімнаті', 'температура'),
        SET_TEMP: ('зроби температуру', 'встанови температуру'),
        TURN_ON_LIGHT: ('увімкни світло у',),
        TURN_OFF_LIGHT: ('вимкни світло у',),
        TURN_ON_ALL_LIGHT: ('увімкни світло у всій квартирі',),
        TURN_OFF_ALL_LIGHT: ('вимкни світло у', 'розпочалась комендантська година'),
        GET_LIGHT: ('де зараз увімкнені лампи', 'які лампи увімкнено', 'які лампи зараз увімкнено'),
        CONDITIONER_STATE: ('в якому стані зараз кондиціонер', 'статус кондиціонера'),
        HOME_STATE: ('в якому стані зараз квартира', 'статус квартири'),
        PATRIOT: ('Слава Україні',),
        KNT: (str(KNT),),
        SAVE: ('збережи таблицю',),
    }
}
