from hotel_management.hotel import Room
from hotel_management.order import OrderItem, Order, Cash, CashPaymentStrategy, OrderBuilder, CreditCard, \
    CreditCardPaymentStrategy
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
        self.room = Room(1, 1000, 101, 'Double')
        self.order_item = OrderItem(self.room)
        self.order_items = []
        self.order_items.append(OrderItem(self.room))

    def test_builder(self):
        order = OrderBuilder(self.customer).check_in_date(1).check_out_date(3).set_order_items(self.order_items).build()
        assert order.customer.id == 1
        assert order.customer.name == 'Duncan'
        assert order.customer.is_loyal is False
        assert order.check_in_date == 1
        assert order.check_out_date == 3
        assert len(order.order_items) == 1
        assert order.order_items[0].item.id == 1
        assert order.order_items[0].item.price == 1000
        assert order.order_items[0].get_sum(order.check_in_date, order.check_out_date) == 2000
        assert order.get_total() == 2000


class TestCashPaymentStrategy:
    def setup(self):
        self.cash = Cash()
        self.cash_payment_strategy = CashPaymentStrategy(self.cash)

    def test_pay(self):
        assert self.cash_payment_strategy.pay(1000) == 'Processing 1000 in cash'


class TestCreditCard:
    def setup(self):
        self.credit_card = CreditCard('1234 5678 9101 2131 4156')

    def test_init(self):
        assert self.credit_card._number == '1234 5678 9101 2131 4156'

    def test_get_number(self):
        assert self.credit_card.get_number() == '1234 5678 9101 2131 4156'


class TestCreditCardPaymentStrategy:
    def setup(self):
        self.credit_card = CreditCard('1234 5678 9101 2131 4156')
        self.credit_card_payment_strategy = CreditCardPaymentStrategy(self.credit_card)

    def test_pay(self):
        assert self.credit_card_payment_strategy.pay(1000) == 'Processing 1000 via credit card 1234 5678 9101 2131 4156'


class TestCashPaymentStrategyWithRealOrder:
    def setup(self):
        self.customer = Customer(1, 'Duncan')
        self.room = Room(1, 1000, 101, 'Double')
        self.order_item = OrderItem(self.room)
        self.order_items = []
        self.order_items.append(OrderItem(self.room))
        self.order = OrderBuilder(self.customer).check_in_date(1).check_out_date(3).set_order_items(self.order_items).\
            build()
        self.cash = Cash()
        self.cash_payment_strategy = CashPaymentStrategy(self.cash)

    def test_pay(self):
        assert self.order.pay(self.cash_payment_strategy) == 'Processing 2000 in cash'
