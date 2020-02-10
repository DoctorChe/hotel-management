from hotel_management.user import Discount, Customer, Administrator


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
