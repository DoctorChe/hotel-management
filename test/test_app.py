from datetime import date

from hotel_management.app import Customer, Room, PeriodicService, OneTimeService, Administrator, Discount


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
        assert self.room.get_time_period_impl(self.check_in_date, self.check_out_date) == (date(2020, 1, 5) -
                                                                                           date(2020, 1, 1))


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
        assert self.periodicservice.get_time_period_impl(self.check_in_date, self.check_out_date) == (date(2020, 1, 5) -
                                                                                                      date(2020, 1, 1))


class TestOneTimeToPeriodAdapter:
    def setup(self):
        self.onetimeservice = OneTimeService(1, 150, 'Transfer')
        self.check_in_date = date(2020, 1, 1)
        self.check_out_date = date(2020, 1, 5)

    def test_init(self):
        assert self.onetimeservice.id == 1
        assert self.onetimeservice.price == 150
        assert self.onetimeservice.title == 'Transfer'

    def test_get_time_period(self):
        assert self.onetimeservice.get_time_period_impl(self.check_in_date, self.check_out_date) == 1


class TestDiscount:
    def setup(self):
        self.discount = Discount()
        self.discount_amount = Discount(amount=15)
        self.discount_loyal = Discount(is_loyal=True)

    def test_init(self):
        assert self.discount.amount == 0
        assert self.discount.is_loyal is False
        assert self.discount_amount.amount == 15
        assert self.discount_amount.is_loyal is False
        assert self.discount_loyal.amount == 0
        assert self.discount_loyal.is_loyal is True

    def test_calc_discount(self):
        assert self.discount.calc_discount() == 0
        assert self.discount_amount.calc_discount() == 15
        assert self.discount_loyal.calc_discount() == 10


class TestCustomer:
    def setup(self):
        self.customer = Customer(1, 'Duncan')

    def test_init(self):
        assert self.customer.id == 1
        assert self.customer.name == 'Duncan'
        assert self.customer.orders is None
        assert self.customer.is_loyal is False

    def test_add_discount_if_not_loyal(self):
        assert self.customer.add_discount() == 0

    def test_add_discount_if_loyal(self):
        self.customer.is_loyal = True
        assert self.customer.add_discount() == 10


class TestAdministrator:
    def setup(self):
        self.admin = Administrator(1)

    def test_init(self):
        assert self.admin.id == 1

    def test_add_discount(self):
        assert self.admin.add_discount(0) == 0
        assert self.admin.add_discount(15) == 15

