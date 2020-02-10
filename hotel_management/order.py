class OrderItem:
    def __init__(self, item):
        self.item = item

    def get_sum(self):
        return self.item.price * self.item.get_time_period


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
        return sum([item.get_sum() for item in self._order_items])

    def add_discount(self, discount):
        pass


class OrderBuilder:
    def __init__(self, customer):
        self.order = Order(customer)

    def check_in_date(self, date):
        self.order._check_in_date = date
        return self

    def check_out_date(self, date):
        self.order._check_out_date = date
        return self

    def add_order_items(self, order_item):
        self.order.order_items.append(order_item)
        return self

    def build(self):
        return self.order
