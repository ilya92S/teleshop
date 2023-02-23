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

    def handle(self):
        """
        Обработчик(декоратор) сообщений, который обрабатывает
        входящие текстовые сообщения от нажатия кнопок.
        """
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            """*****МЕНЮ*****"""
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)
            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)
            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

