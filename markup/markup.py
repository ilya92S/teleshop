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
        Создаем и возвращаем кнопку по входным параметрам.
        """
        if name == "AMOUNT_ORDERS":
            config.KEYBOARD['AMOUNT_ORDERS'] = '{} {} {}'.format(step + 1, ' из ',
                                                                 str(
                                                                     self.BD.count_rows_order()))
        if name == "AMOUNT_PRODUCT":
            config.KEYBOARD["AMOUNT_PRODUCT"] = '{}'.format(quantity)

        return KeyboardButton(config.KEYBOARD[name])

    def start_main_menu(self):
        """Создает разметку выбора роли в магазине."""
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn("BUYER'S MENU")
        itm_btn_2 = self.set_btn("MANAGER MENU")
        itm_btn_3 = self.set_btn("ADMIN MENU")
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2)
        self.markup.row(itm_btn_3)
        return self.markup

    def manager_menu(self):
        """Создает разметку кнопок для меню менеджера"""
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('MANAGER_ORDER')
        itm_btn_2 = self.set_btn('BACK_TO_MAIN_MENU')
        self.markup.add(itm_btn_2, itm_btn_1)
        return self.markup

    def admin_menu(self):
        """Создает разметку кнопок для меню админа."""
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('BACK_TO_MAIN_MENU')
        itm_btn_2 = self.set_btn('ADD_PRODUCT')
        itm_btn_3 = self.set_btn('DELETE_PRODUCT')
        self.markup.add(itm_btn_1, itm_btn_2, itm_btn_3)
        return self.markup

    def start_user_menu(self):
        """Создает разметку кнопок в основном меню и возвращает разметку."""
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('CHOOSE_GOODS')
        itm_btn_2 = self.set_btn('INFO')
        itm_btn_3 = self.set_btn('SETTINGS')
        itm_btn_4 = self.set_btn('BACK_TO_MAIN_MENU')
        # ниже будет приветден порядок расположения кнопок
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3)
        self.markup.row(itm_btn_4)
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

    def order_menu(self, step, quantity):
        """
        Создает разметку кнопок в заказе товара и возвращает разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('X', step, quantity)
        itm_btn_2 = self.set_btn('DOUWN', step, quantity)
        itm_btn_3 = self.set_btn('AMOUNT_PRODUCT', step, quantity)
        itm_btn_4 = self.set_btn('UP', step, quantity)

        itm_btn_5 = self.set_btn('BACK_STEP', step, quantity)
        itm_btn_6 = self.set_btn('AMOUNT_ORDERS', step, quantity)
        itm_btn_7 = self.set_btn('NEXT_STEP', step, quantity)
        itm_btn_8 = self.set_btn('APPLAY', step, quantity)
        itm_btn_9 = self.set_btn('<<', step, quantity)
        # расположение кнопок в меню
        self.markup.row(itm_btn_1, itm_btn_2, itm_btn_3, itm_btn_4)
        self.markup.row(itm_btn_5, itm_btn_6, itm_btn_7)
        self.markup.row(itm_btn_9, itm_btn_8)

        return self.markup