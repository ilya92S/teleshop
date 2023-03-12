import os
from emoji import emojize

TOKEN = '5976169619:AAG2ni-VRyjkHXfG5NO3Y0UfnaFKW6pyo0k'
NAME_BD = 'products.db'
VERSION = '0.0.1'
AUTHOR = 'ILYA'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join('sqlite:///' + BASE_DIR, NAME_BD)
COUNT = 0
unicode_emoji = {
    'personal computer': '\U0001F4BB',
    'package': '\U0001F4E6',
    'white right pointing backhand index': '\U0001F449'
}

KEYBOARD = {
    'DELETE_PRODUCT': emojize('Удвлить продукт'),
    'ADD_PRODUCT': emojize(':pencil: Добавить продукт'),
    'MANAGER_ORDER': emojize('Проверить наличие заказов'),
    'BACK_TO_MAIN_MENU': emojize('Выбор роли пользователя'),
    "ADMIN MENU": emojize(unicode_emoji['personal computer'] + 'Меню администратора'),
    "MANAGER MENU": emojize(unicode_emoji['package'] + 'Меню менеджера'),
    "BUYER'S MENU": emojize(unicode_emoji['white right pointing backhand index'] + 'Меню покупателя'),
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О магазине'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'SEMIPRODUCT': emojize(':pizza: Полуфабрикаты'),
    'GROCERY': emojize(':bread: Бакалея'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженое'),
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
    'SEMIPRODUCT': 1,
    'GROCERY': 2,
    'ICE_CREAM': 3
} # id категории продуктв

COMMANDS = {
    'START': 'start',
    'HELP': 'help'
} # название команд
