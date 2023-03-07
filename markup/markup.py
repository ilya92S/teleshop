from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,\
    InlineKeyboardMarkup, InlineKeyboardButton
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

    def info_menu(self):
        """
        Создаем разметку кнопок в меню "О магазине"
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        self.markup.row(itm_btn_1)
        return self.markup

    def settings_menu(self):
        """
        Создаем разметку кнопок в меню "Настройки"
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        self.markup.row(itm_btn_1)
        return self.markup

    @staticmethod
    def remove_menu():
        """
        Удаляет меню
        """
        return ReplyKeyboardRemove()

    def category_menu(self):
        """
        Создает разметку кнопок в меню категорий товара и возвращает разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('SEMIPRODUCT')
        itm_btn_2 = self.set_btn('GROCERY')
        itm_btn_3 = self.set_btn('ICE_CREAM')
        itm_btn_4 = self.set_btn('<<')
        itm_btn_5 = self.set_btn('ORDER')
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        self.markup.row(itm_btn_3)
        self.markup.row(itm_btn_4, itm_btn_5)
        return self.markup

    def set_select_category(self, category):
        """
        Создает разметку инлайн-кнопок в выбранной
        категории товара и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        # загружаем в названия инлайн-кнопок данные
        # из БД в соответствии с категорией товара
        for itm in self.BD.select_all_product_category(category):
            self.markup.add(self.set_inline_btn(itm))

        return self.markup

    @staticmethod
    def set_inline_btn(name):
        """
        Создает и возвращает инлайн кнопку по входным параметрам
        """
        return InlineKeyboardButton(str(name), callback_data=str(name.id))
