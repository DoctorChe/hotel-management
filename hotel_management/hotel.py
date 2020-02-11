import abc


class Hotel:
    def __init__(self):
        self.rooms = []
        self.services = []

    def add_room(self, id_, price, number, type_):
        self.rooms.append(Room(id_, price, number, type_))

    def add_service(self, id_, price, title):
        self.rooms.append(Service(id_, price, title))


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
