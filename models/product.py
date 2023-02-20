from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from models.category import Category
Base = declarative_base() # декларативный стиль описания сущности


class Product(Base):
    """
    Класс для создания таблицы "Товар".
    Attributes
        __tablename__: название таблицы
        id: поле id
        name: поле названия товара
        title: поле названия торговой марки
        price: поле цена
        quantity: поле количество
        is_active: поле наличия товара для продажи
        category_id: поле ссылка на внешнюю таблицу с названием поля id
        category: поле категория для каскадного удаления товаров
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    title = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    is_active = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))

    category = relationship(Category, backref=backref('product', uselist=True, cascade='delete, all'))

    def __str__(self):
        """ Метод возвращает строковое представление объекта класса. """
        return f'{self.name} {self.title} {self.price}'
    