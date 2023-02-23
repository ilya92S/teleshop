from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from settings import config
from data_base.dbalchemy import DBManager


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """
    def __init__(self):
        self.markup = None
        self.BD = DBManager()

    def set_btn(self, name, step=0, quantity=0):
        """
        Создаем и возвращаем кнопку по входным параметрам
        """
        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        """Создает разметку кнопок в основном меню и возвращает разметку."""
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('CHOOSE_GOODS')
        itm_btn_2 = self.set_btn('INFO')
        itm_btn_3 = self.set_btn('SETTINGS')
        # ниже будет приветден порядок расположения кнопок
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3)
        return self.markup
