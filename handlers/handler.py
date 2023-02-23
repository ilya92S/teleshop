import abc
from markup.markup import Keyboards
from data_base.dbalchemy import DBManager


class Handler(metaclass=abc.ABCMeta):
    """
    Базовый абстрактный класс обработчик.
    """
    def __init__(self, bot):
        """
        self.bot: объект бота
        self.keybords: инициализация разметки кнопок
        self.BD: инициализируем менеджер для работы с БД
        """
        self.bot = bot
        self.keybords = Keyboards()
        self.BD = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass
