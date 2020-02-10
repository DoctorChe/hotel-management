from hotel_management.hotel import Room
from hotel_management.order import OrderItem, Order
from hotel_management.user import Customer


class TestOrderItem:
    def setup(self):
        self.room = Room(1, 1000, 101, 'Double')
        self.order_item = OrderItem(self.room)


class TestOrder:
    def setup(self):
        self.room = Room(1, 1000, 101, 'Double')
        self.order_item = OrderItem(self.room)
        self.customer = Customer(1, 'Duncan')
        self.order = Order(self.customer)

    def test_init(self):
        assert self.order.order_items is None
        assert self.order.check_in_date is None
        assert self.order.check_out_date is None


class TestOrderBuilder:
    def setup(self):
        self.customer = Customer(1, 'Duncan')

    # def
