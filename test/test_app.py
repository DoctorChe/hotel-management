from datetime import date

from hotel_management.app import Customer, Room, PeriodicService, OneTimeService, OneTimeToPeriodAdapter


class TestCustomer:

    def setup(self):
        self.customer = Customer(1, 'John')

    def test_init(self):
        assert self.customer.id == 1
        assert self.customer.name == 'John'


class TestRoom:
    def setup(self):
        self.room = Room(1, 1000, 101, 'Double')
        self.check_in_date = date(2020, 1, 1)
        self.check_out_date = date(2020, 1, 5)

    def test_init(self):
        assert self.room.id == 1
        assert self.room.price == 1000
        assert self.room.number == 101
        assert self.room.type == 'Double'

    def test_get_time_period(self):
        assert self.room.get_time_period(self.check_in_date, self.check_out_date) == date(2020, 1, 5) - date(2020, 1, 1)


class TestPeriodicService:
    def setup(self):
        self.periodicservice = PeriodicService(1, 100, 'Breakfast')
        self.check_in_date = date(2020, 1, 1)
        self.check_out_date = date(2020, 1, 5)

    def test_init(self):
        assert self.periodicservice.id == 1
        assert self.periodicservice.price == 100
        assert self.periodicservice.title == 'Breakfast'

    def test_get_time_period(self):
        assert self.periodicservice.get_time_period(self.check_in_date, self.check_out_date) == (date(2020, 1, 5) -
                                                                                                 date(2020, 1, 1))


class TestOneTimeToPeriodAdapter:
    def setup(self):
        self.onetimeservice = OneTimeService(1, 150, 'Transfer')
        self.adapter = OneTimeToPeriodAdapter(self.onetimeservice)
        self.check_in_date = date(2020, 1, 1)
        self.check_out_date = date(2020, 1, 5)

    def test_init(self):
        assert self.onetimeservice.id == 1
        assert self.onetimeservice.price == 150
        assert self.onetimeservice.title == 'Transfer'

    def test_get_time_period(self):
        assert self.adapter.get_time_period(self.check_in_date, self.check_out_date) == 1
