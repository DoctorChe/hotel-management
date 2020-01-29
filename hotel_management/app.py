class Item:
    def __init__(self, id_, price):
        self.id = id_
        self.price = price

    @staticmethod
    def get_time_period(check_in_date, check_out_date):
        return check_out_date - check_in_date


class Room(Item):
    def __init__(self, id_, price, number, type_):
        super().__init__(id_, price)
        self.number = number
        self.type = type_


class Service(Item):
    def __init__(self, id_, price, title):
        super().__init__(id_, price)
        self.title = title


class PeriodicService(Service):
    pass


class OneTimeService(Service):
    pass


class OneTimeToPeriodAdapter(OneTimeService):
    def __init__(self, adaptee):
        self._adaptee = adaptee

    @staticmethod
    def get_time_period(check_in_date, check_out_date):
        return 1


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
    def __init__(self, customer):
        self.order = Order(customer)

    def check_in_date(self, date):
        self.order._check_in_date = date
        return self

    def check_out_date(self, date):
        self.order._check_out_date = date
        return self

    def add_room(self, room):
        self.order.rooms.append(room)
        return self

    def add_extra_service(self, service):
        self.order.extra_services.append(service)
        return self

    def build(self):
        return self.order


class User:
    def __init__(self, id_):
        self.id = id_


class Customer(User):
    def __init__(self, id_, name):
        super().__init__(id_)
        self.name = name


class Administrator(User):
    def __init__(self, id_):
        super().__init__(id_)
