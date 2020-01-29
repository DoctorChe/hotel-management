from hotel_management.app import Customer, Room, PeriodicService, OneTimeService


class TestCustomer:

    def setup(self):
        self.customer = Customer(1, 'John')

    def test_init(self):
        assert self.customer.id == 1
        assert self.customer.name == 'John'


class TestRoom:
    def setup(self):
        self.room = Room(1, 1000, 101, 'Double')

    def test_init(self):
        assert self.room.id == 1
        assert self.room.price == 1000
        assert self.room.number == 101
        assert self.room.type == 'Double'


class TestPeriodicService:
    def setup(self):
        self.periodicservice = PeriodicService(1, 100, 'Breakfast')

    def test_init(self):
        assert self.periodicservice.id == 1
        assert self.periodicservice.price == 100
        assert self.periodicservice.title == 'Breakfast'


class TestOneTimeToPeriodAdapter:
    def setup(self):
        self.onetimeservice = OneTimeService(1, 150, 'Transfer')

    def test_init(self):
        assert self.onetimeservice.id == 1
        assert self.onetimeservice.price == 150
        assert self.onetimeservice.title == 'Transfer'

