from hotel_management.app import Customer


class TestCustomer:

    def setup(self):
        self.customer = Customer(1, 'John')

    def test_init(self):
        assert self.customer.id == 1
        assert self.customer.name == 'John'
