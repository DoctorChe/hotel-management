import abc


class OrderItem:
    def __init__(self, item):
        self.item = item

    def get_sum(self, check_in_date, check_out_date):
        return self.item.price * self.item.get_time_period_impl(check_in_date, check_out_date)


class Order:
    def __init__(self, customer):
        self.customer = customer
        self._order_items = None
        self._check_in_date = None
        self._check_out_date = None

    @property
    def order_items(self):
        return self._order_items

    @property
    def check_in_date(self):
        return self._check_in_date

    @property
    def check_out_date(self):
        return self._check_out_date

    def get_total(self):
        return sum([item.get_sum(self.check_in_date, self.check_out_date) for item in self._order_items])

    def add_discount(self, discount):
        pass

    def pay(self, strategy):
        total = self.get_total()
        return strategy.pay(total)


class OrderBuilder:
    def __init__(self, customer):
        self.order = Order(customer)

    def check_in_date(self, date):
        self.order._check_in_date = date
        return self

    def check_out_date(self, date):
        self.order._check_out_date = date
        return self

    def set_order_items(self, order_items):
        self.order._order_items = order_items
        return self

    def build(self):
        return self.order


# Strategy pattern
class PaymentStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def pay(self, amount):
        pass


class Cash:
    pass


class CashPaymentStrategy(PaymentStrategy):
    def __init__(self, cash):
        # self.cash = cash
        pass

    def pay(self, amount):
        return f'Processing {amount} in cash'


class CreditCard:
    def __init__(self, number):
        self._number = number

    def get_number(self):
        return self._number


class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card):
        self.card = card

    def pay(self, amount):
        return f'Processing {amount} via credit card {self.card.get_number()}'
