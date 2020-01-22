class Item:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @staticmethod
    def get_time_period(check_in_date, check_out_date):
        return check_out_date - check_in_date


class OrderItem:
    def __init__(self, item):
        self.item = item

    def get_sum(self):
        return self.item.price * self.item.get_time_period


class Order:
    def __init__(self, customer):
        self.customer = customer
        self._rooms = None
        self._extra_services = None
        self._check_in_date = None
        self._check_out_date = None

    @property
    def rooms(self):
        return self._rooms

    @property
    def extra_services(self):
        return self._extra_services

    def get_total(self):
        return sum([item.get_sum() for item in (*self._rooms, *self._extra_services)])

    def add_discount(self, discount):
        pass


class OrderBuilder:
    """
    Построитель заказа
    """

    def __init__(self, customer):
        self.order = Order(customer)

    def check_in_date(self, date):
        self.order._check_in_date = date

    def check_out_date(self, date):
        self.order._check_out_date = date

    def add_room(self, room):
        self.order.rooms.append(room)

    def add_extra_service(self, service):
        self.order.extra_services.append(service)
