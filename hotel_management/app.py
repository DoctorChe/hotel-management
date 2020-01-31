import abc

DISCOUNT_STANDARD = 10


class AbstractItem:
    def __init__(self, implementor):
        self._implementor = implementor

    def get_time_period(self, check_in_date, check_out_date):
        return self._implementor.get_time_period_impl(check_in_date, check_out_date)


class ItemImplementor(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def get_time_period_impl(check_in_date, check_out_date):
        pass


class Item(ItemImplementor):
    def __init__(self, id_, price):
        self.id = id_
        self.price = price

    @staticmethod
    def get_time_period_impl(check_in_date, check_out_date):
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
    @staticmethod
    def get_time_period_impl(check_in_date, check_out_date):
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


class UserInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_order(self):
        pass

    @abc.abstractmethod
    def add_discount(self):
        pass


class User(UserInterface):
    def __init__(self, id_):
        self.id = id_

    def create_order(self):
        pass

    def add_discount(self):
        pass


class Customer(User):
    DISCOUNT = {
        0: 0,
        1: DISCOUNT_STANDARD
    }

    def __init__(self, id_, name):
        super().__init__(id_)
        self.name = name
        self.orders = None
        self.is_loyal = False

    def add_discount(self):
        return __class__.DISCOUNT[self.is_loyal]


class CreateDiscount:
    def __init__(self, amount):
        self.amount = amount

    def __call__(self, *args, **kwargs):
        return self.amount


class Administrator(User):
    def __init__(self, id_):
        super().__init__(id_)

    # def add_discount(self):
    #     return CreateDiscount(amount=0).amount
