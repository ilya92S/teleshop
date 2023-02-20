from telebot.types import KeyboardButton
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
        Создаем и возвращаем кнопку по входдным параметрам
        """
        return KeyboardButton(config.KEYBOARD[name])
