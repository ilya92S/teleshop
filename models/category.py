from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base # декларативный стиль описания сущности


class Category(Base):
    """
    Класс для описания таблицы "Категория товаров".
    Attributes
        __tablename__: название таблицы
        id: поле id
        name: поле названия категории
        is_active: поле наличия категории
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __str__(self):
        """ Метод возвращает строковое представление объекта класса. """
        return self.name

