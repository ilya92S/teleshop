from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_base.dbcore import Base

from settings import config
from models.product import Product


class Singleton(type):
    """
    Паттерн Singleton представляет механизм создания одного
    и только одного объекта класса,
    и предоставляет к нему глобальную точку доступа.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """
    Класс менеджер для работы с БД.
    Метакласс Singleton контролирует поведение класса DBManager, так
    чтобы для класса DBManager всегда создавался один и тот же объект.
    """
    def __init__(self):
        """
        Инициализация сессии и подключение к БД
        """
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_product_category(self, category):
        """
        Возвращает все товары категории
        """
        id = 0
        if category[2::] == 'Полуфабрикаты':
            id = 1
        elif category[2::] == 'Бакалея':
            id = 2
        elif category[2::] == 'Мороженое':
            id = 3
        result = self._session.query(Product).filter_by(
            category_id=id).all()
        self.close()
        return result

    def close(self):
        """Закрывает ссесию"""
        self._session.close()
