import os
from emoji import emojize

TOKEN = '5976169619:AAG2ni-VRyjkHXfG5NO3Y0UfnaFKW6pyo0k'
NAME_BD = 'products.db'
VERSION = '1.0.1'
AUTHOR = 'ilya92S'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join('sqlite:///' + BASE_DIR, NAME_BD)
COUNT = 0

UNICODE_EMOJI = {
    'open_file': '\U0001F4C2',
    'info': '\U0001F4AC',
    'settings': '\U00002699',
    'laptop': '\U0001F4BB',
    'desktop': '\U0001F5A5',
    'printer': '\U0001F5A8'
}

KEYBOARD = {
    'CHOOSE_GOODS': emojize(UNICODE_EMOJI['open_file'] + 'Выбрать товар'),
    'INFO': emojize(UNICODE_EMOJI['info'] + 'О магазине'),
    'SETTINGS': emojize(UNICODE_EMOJI['settings'] + 'Настройки'),
    'LAPTOP': emojize(UNICODE_EMOJI['laptop'] + 'Ноутбуки'),
    'DESKTOP': emojize(UNICODE_EMOJI['desktop'] + 'Стационарные компьютеры'),
    'PRINTER': emojize(UNICODE_EMOJI['printer'] + 'Принтеры'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOUWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLAY': '✅ Оформить заказ',
    'COPY': '©️'
}

CATEGORY = {
    'LAPTOP': 1,
    'DESKTOP': 2,
    'PRINTER': 3
} # id категории продуктв

COMMANDS = {
    'START': 'start',
    'HELP': 'help'
} # название команд
