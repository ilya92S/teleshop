from handlers.handler import Handler


class HandlerCommands(Handler):

    """Класс обрабатывает входящие команды"""

    def __init__(self, bot):
        super().__init__(bot)

    def press_btn_start(self, message):
        """Обрабатывает входящие /start команды"""

        self.bot.send_message(message.chat.id, f'{message.from_user.first_name},'
                                               f' здравствуйте! Жду дальнейших задач.',
                              reply_markup=self.keybords.start_main_menu())

    def handle(self):
        """Обработчик(декоратор) сообщений, который обрабатывает входящие /start команды."""

        @self.bot.message_handler(commands=['start'])
        def handle(message):
            print(f'команда {message.text} была отловлена обработчиком событий', message.from_user.id, message.from_user.first_name)
            if message.text == '/start':
                self.press_btn_start(message)
