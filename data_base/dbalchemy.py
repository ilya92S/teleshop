from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_base.dbcore import Base

from settings import config, utility
from models.product import Product
from models.order import Order
import datetime


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

    def _add_orders(self, quantity, product_id, user_id):
        """
        Метод заполнения заказа
        """
        # получаем список всех product_id
        all_id_product = self.select_all_product_id()
        # если данные есть в списке, обновляем таблицы заказа и продуктов
        if product_id in all_id_product:
            quantity_order = self.select_order_quantity(product_id)
            quantity_order += 1
            self.update_order_value(product_id, 'quantity', quantity_order)

            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
            return
        # если данных нет создаем новый объект заказа
        else:
            order = Order(quantity=quantity, product_id=product_id,
                          user_id=user_id, data=datetime.datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)

        self._session.add(order)
        self._session.commit()
        self.close()

    def select_all_product_id(self):
        """
        Возвращаем все id товара в заказе
        """
        result = self._session.query(Order.product_id).all()
        self.close()
        # конвертируем результат выборки на вид [1, 3, 5, ...]
        return utility._convert(result)

    def select_order_quantity(self, product_id):
        """
        Возвращает количество товара в заказе
        """
        result = self._session.query(Order).filter_by(
            product_id=product_id).one()
        self.close()
        return result.quantity

    def update_order_value(self, product_id, name, value):
        """
        Обновляет данные указанной позиции заказа
        в соответствии с номером товара - rownum
        """
        self._session.query(Order).filter_by(
            product_id=product_id).update({name: value})
        self.close()

    def select_single_product_quantity(self, rownum):
        """
        Возвращает количество товара на складе
        в соответствии с номером товара - rownum
        Этот номер определяется при выборе товара в интерфейсе.
        """
        result = self._session.query(
            Product.quantity).filter_by(id=rownum).one()
        self.close()
        return result.quantity

    def update_product_value(self, rownum, name, value):
        """
        Обновляет количество товара на складе
        в соответствии с номером товара - rownum
        """
        self._session.query(Product).filter_by(id=rownum).update({name: value})
        self._session.commit()
        self.close()

    def select_single_product_name(self, rownum):
        """
        Возвращает название товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Product.name).filter_by(id=rownum).one()
        self.close()
        return result.name

    def select_single_product_title(self, rownum):
        """
        Возвращает торговую марку товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Product.title).filter_by(id=rownum).one()
        self.close()
        return result.title

    def select_single_product_price(self, rownum):
        """
        Возвращает цену товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Product.price).filter_by(id=rownum).one()
        self.close()
        return result.price

