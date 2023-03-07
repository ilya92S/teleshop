from settings.message import MESSAGES
from settings import config
from handlers.handler import Handler


class HandlerAllText(Handler):
    """Класс обрабатывает входящие текствое сообщения от нажатия на кнопку"""

    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_info(self, message):
        """
        Обрабатывает входящие текствовые сообщения
        от нажатия на кнопку "О магазине".
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode='HTML',
                              reply_markup=self.keybords.info_menu())

    def pressed_btn_settings(self, message):
        """
        Обрабатывает входящие текствовые сообщения
        от нажатия на кнопку "Настройки".
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode='HTML',
                              reply_markup=self.keybords.settings_menu())

    def pressed_btn_back(self, message):
        """
        Обрабатывает входящие текстовые сообщения
        от нажатия на кнопку "Назад".
        """
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keybords.start_menu())

    def pressed_btn_category(self, message):
        """
        Обработка событий нажатия на кнопку "Выбрать товар".
        Выбор категории товаров.
        """
        self.bot.send_message(message.chat.id, "Каталог категорий товара",
                              reply_markup=self.keybords.remove_menu())
        self.bot.send_message(message.chat.id, "Сделайте свой выбор",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_product(self, message, product):
        """
        Обработка событий нажатия на кнопку "Выбрать товар".
        Точнее это выбор товара из категории.
        """
        self.bot.send_message(message.chat.id, "Категория" +
                              config.KEYBOARD[product],
                              reply_markup=self.keybords.set_select_category
                              (config.KEYBOARD[product]))
        self.bot.send_message(message.chat.id, "Ok",
                              reply_markup=self.keybords.category_menu())

    def handle(self):
        """
        Обработчик(декоратор) сообщений, который обрабатывает
        входящие текстовые сообщения от нажатия кнопок.
        """
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            print(f'команда {message.text} была отловлена обработчиком событий', message.from_user.id,
                  message.from_user.first_name)

            """*****ГЛАВНОЕ МЕНЮ*****"""
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            """*****меню(категория товара, ПФ, Бакалея, Мороженное)*****"""
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')
