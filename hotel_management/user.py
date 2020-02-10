import abc

from hotel_management.order import OrderBuilder


class UserInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_order(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def add_discount(self, *args, **kwargs):
        pass


class User(UserInterface):
    def __init__(self, id_):
        self.id = id_

    def create_order(self, *args, **kwargs):
        pass

    def add_discount(self, *args, **kwargs):
        pass


class Customer(User):
    def __init__(self, id_, name):
        super().__init__(id_)
        self.name = name
        self.orders = None
        self.is_loyal = False

    def create_order(self, check_in_date, check_out_date, room, service):
        return OrderBuilder(self).check_in_date(check_in_date).check_out_date(check_out_date).add_room(room).\
            add_extra_service(service).build()

    def add_discount(self):
        return Discount(is_loyal=self.is_loyal).calc_discount()


class Administrator(User):
    def __init__(self, id_):
        super().__init__(id_)

    @staticmethod
    def create_order(customer, check_in_date, check_out_date, room, service):
        return OrderBuilder(customer).check_in_date(check_in_date).check_out_date(check_out_date).add_room(room).\
            add_extra_service(service).build()

    def add_discount(self, amount):
        return Discount(amount=amount).calc_discount()


class Discount:
    DISCOUNT_STANDARD = 10

    DISCOUNT = {
        False: 0,
        True: DISCOUNT_STANDARD
    }

    def __init__(self, amount=0, is_loyal=False):
        self.amount = amount
        self.is_loyal = is_loyal

    def calc_discount(self):
        return max(self.amount, self.DISCOUNT[self.is_loyal])
