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

    def handle(self):
        """
        Обработчик(декоратор) сообщений, который обрабатывает
        входящие текстовые сообщения от нажатия кнопок.
        """
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            print(f'команда {message.text} была отловлена обработчиком событий', message.from_user.id,
                  message.from_user.first_name)

            """*****ГЛАВНОЕ МЕНЮ*****"""
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            """*****меню(категория товара, ПФ, Бакалея, Мороженное)*****"""
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            """******ОБРАБАТЫВАЕМ СООБЩЕНИЕ -ЗАКАЗ-*****"""
            if message.text == config.KEYBOARD['ORDER']:
                # если заказ есть
                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat_id, MESSAGES['no_orders'],
                                          parse_mode='HTML',
                                          reply_markup=self.keybords.category_menu())

            """*****ИНТЕРФЕЙС РЕДАКТИРОВАНИЯ ЗАКАЗА*****"""

            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)
            if message.text == config.KEYBOARD['DOUWN']:
                self.pressed_btn_douwn(message)




