from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import config
from models.product import Product
Base = declarative_base()

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
        result = self._session.query(Product).filter_by(
            category_id=category).all()

        self.close()
        return result

    def close(self):
        """Закрывает ссесию"""
        self._session.close()