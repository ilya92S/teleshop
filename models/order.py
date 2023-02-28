from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from models.product import Product
from data_base.dbcore import Base


class Order(Base):
    """
    Класс для создания таблицы "Заказ".
    Attributes
        __tablename__: название таблицы
        id: поле id
        quantity: поле количество товаров в заказе
        data: время создания заказа
        product_id: поле привязки к внешней таблицы к id товара с внешней таблицы products
        user_id: поле id клиента
        product: для каскадного удаления данных из таблицы
            (если нет товара то удвляем все записи в заказе по нему)
    """

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    data = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id')) # привязка к полю id таблицы products
    user_id = Column(Integer)

    product = relationship(Product, backref=backref('orders', uselist=True, cascade='delete,all'))

    def __str__(self):
        """ Метод возвращает строковое представление объекта класса. """
        return f'{self.quantity} {self.data}'

