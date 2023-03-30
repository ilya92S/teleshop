from settings.message import MESSAGES
from settings import config
from handlers.handler import Handler
from settings import utility


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

    def pressed_btn_order(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку "Заказ".
        """
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество по каждой позиции товара в заказе
        quantity = self.BD.select_order_quantity(count[self.step])
        # отпраавляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю при выполнении различных действий
        """
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(
            self.step + 1), parse_mode='HTML')
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].
                              format(self.BD.select_single_product_name(product_id),
                                     self.BD.select_single_product_title(product_id),
                                     self.BD.select_single_product_price(product_id),
                                     self.BD.select_order_quantity(product_id)),
                              parse_mode='HTML',
                              reply_markup=self.keybords.order_menu(
                                  self.step, quantity))

    def pressed_btn_up(self, message):
        """
        Обработка нажатия кнопки увеличения
        количества определенного товара в заказе.
        """
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество единиц текущей товарной позиции заказа
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # получаем количество данного товара на складе
        quantity_product = self.BD.select_single_product_quantity(count[self.step])

        # если товар есть
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            # вносим изменение в БД orders
            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)
            # вносим изменение в БД product
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_douwn(self, message):
        """
        Обработка нажатия кнопки уменьшения
        количества определенного товара в заказе
        """
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество единиц текущей товарной позиции заказа
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # получаем количество данного товара на складе
        quantity_product = self.BD.select_single_product_quantity(count[self.step])

        # если товар есть
        if quantity_product > 0:
            quantity_order -= 1
            quantity_product += 1
            # вносим изменение в БД orders
            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)
            # вносим изменение в БД product
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
            # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        """
        Обдрабатывает нажатие кнопки удаление товара в заказе
        """
        # получаем список всех product_id заказа
        count = self.BD.select_all_product_id()

        # если список не пуст
        if count.__len__() > 0:
            # получаем количество конкретной позиции в заказе
            quantity_order = self.BD.select_order_quantity(count[self.step])
            # получаем количество товара конкретной позиции на складе
            quantity_product = self.BD.select_single_product_quantity(count[self.step])
            # возвращаем количество товара из заказа обратно на склад
            quantity_product += quantity_order
            # вносим изменения в БД orders
            self.BD.delete_order(count[self.step])
            # вносим изменение в БД product
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
            # уменьшаем шаг
            self.step -= 1

        count = self.BD.select_all_product_id()

        # если список не пуст
        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step])
            # отправляем пользоватлю сообщение
            self.send_message_order(count[self.step], quantity_order, message)

        else:
            # если товара нет в заказе отправляем сообщение
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode='HTML',
                                  reply_markup=self.keybords.category_menu())

    def pressed_btn_back_step(self, message):
        """
        Обрабатывает нажатие кнопки перемещение на
        предыдущую позицию товара в заказе
        """
        if self.step > 0:
            self.step -= 1
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_next_step(self, message):
        """
        Обрабатывает нажатие кнопки перемещения
        на следующую позицию товара в заказе
        """
        # увеличиваем шаг пока он не будет равен количеству строк
        # заказ с расчетом цены деления начиная с "0"
        if self.step < self.BD.count_rows_order() -1 :
            self.step += 1
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количества конкретного товара
        # в соответствии с шагом выборки
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_applay(self, message):
        """
        Обрабатывает входящие текстовые сообщения
        от нажатия на кнопку "Оформить заказ".
        """
        # отправляем ответ пользователю
        self.bot.send_message(message.chat.id,
                              MESSAGES['applay'].format(
                                  utility.get_total_coas(self.BD),
                                  utility.get_total_quantity(self.BD)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.category_menu()

                              )
        # очищаем данные с заказа
        self.BD.delete_all_order()

    def handle(self):
        """
        Обработчик(декоратор) сообщений, который обрабатывает
        входящие текстовые сообщения от нажатия кнопок.
        """
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # print(f'{message.chat.first_name}, нажал на кнопку {message.text}')

            """*****ГЛАВНОЕ МЕНЮ*****"""
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            """*****меню(категория товаров Ноутбуки, Компьютеры, Принтеры)*****"""
            if message.text == config.KEYBOARD['LAPTOP']:
                self.pressed_btn_product(message, 'LAPTOP')

            if message.text == config.KEYBOARD['DESKTOP']:
                self.pressed_btn_product(message, 'DESKTOP')

            if message.text == config.KEYBOARD['PRINTER']:
                self.pressed_btn_product(message, 'PRINTER')

            """******ОБРАБАТЫВАЕМ СООБЩЕНИЕ -ЗАКАЗ-*****"""
            if message.text == config.KEYBOARD['ORDER']:
                # если заказ есть
                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                          parse_mode='HTML',
                                          reply_markup=self.keybords.category_menu())

            """*****ИНТЕРФЕЙС РЕДАКТИРОВАНИЯ ЗАКАЗА*****"""

            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)
            if message.text == config.KEYBOARD['DOUWN']:
                self.pressed_btn_douwn(message)
            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)
            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)
            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)
            if message.text == config.KEYBOARD['APPLAY']:
                self.pressed_btn_applay(message)
            # иные нажатия и ввод дынных пользователем
            else:
                self.bot.send_message(message.chat.id, message.text)
