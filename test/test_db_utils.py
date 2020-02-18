import datetime
import os
import sqlite3

import pytest

from hotel_management.db_utils import create_db, CustomerMapper, RecordNotFoundException, DbUpdateException, ItemDM, \
    RoomDM, OrderDM
from hotel_management.domain_model import Int, String, DecimalField, Date, FieldCollection
from hotel_management.user import Customer

DB_TEST_PATH = 'db_test.sqlite'


class TestCustomerMapper:
    def setup(self):
        create_db(DB_TEST_PATH)
        self.connection = sqlite3.connect(DB_TEST_PATH)
        self.customer_mapper = CustomerMapper(self.connection)
        self.customer_1 = Customer(1, 'Duncan')
        self.customer_2 = Customer(1, 'Scotch')

    def teardown(self):
        self.connection.close()
        os.remove(DB_TEST_PATH)

    def test_find_by_id(self):
        self.customer_mapper.insert(self.customer_1)
        customer = self.customer_mapper.find_by_id(1)
        assert customer.__dict__ == {'id': 1, 'name': 'Duncan', 'orders': None, 'is_loyal': False}

    def test_update(self):
        self.customer_mapper.insert(self.customer_1)
        self.customer_mapper.update(self.customer_2)
        customer = self.customer_mapper.find_by_id(1)
        assert customer.__dict__ == {'id': 1, 'name': 'Scotch', 'orders': None, 'is_loyal': False}

    def test_delete(self):
        self.customer_mapper.insert(self.customer_1)
        self.customer_mapper.delete(self.customer_1)
        with pytest.raises(RecordNotFoundException):
            self.customer_mapper.find_by_id(1)


class TestItemDM:
    def setup(self):
        self.item_1 = ItemDM(id=1, price=1000.00, )
        self.item_2 = ItemDM(id=2, price=99.99, )
        self.item_3 = ItemDM(id=2, price=99.99, )

    def test_domain_model(self):
        assert self.item_1.__slots_optimization__ is True
        assert self.item_1.__slots__ == ('_id', '_price')
        assert self.item_2 == self.item_3
        assert isinstance(self.item_1.__fields__['id'], Int) is True
        assert isinstance(self.item_1.__fields__['price'], DecimalField) is True


# class TestRoomDM:
#     def setup(self):
#         self.room_1 = RoomDM(id=1, price=1000.00, number=101, type='Single')
#
#     def test_domain_model(self):
#         assert self.room_1.__slots__ == ('_number', '_type')
#         assert isinstance(self.room_1.__fields__['number'], Int) is True
#         assert isinstance(self.room_1.__fields__['type'], String) is True
#         assert self.room_1.get_data()['number'] == 101
#         assert self.room_1.get_data()['type'] == 'Single'


class TestRoomDM:
    def setup(self):
        self.room_1 = RoomDM(id=1, price=1000.00, number=101, type='Single')

    def test_domain_model(self):
        assert self.room_1.__slots__ == ('_id', '_price', '_number', '_type')
        assert isinstance(self.room_1.__fields__['id'], Int) is True
        assert isinstance(self.room_1.__fields__['price'], DecimalField) is True
        assert isinstance(self.room_1.__fields__['number'], Int) is True
        assert isinstance(self.room_1.__fields__['type'], String) is True
        assert self.room_1.get_data()['id'] == 1
        assert self.room_1.get_data()['price'] == 1000.00
        assert self.room_1.get_data()['number'] == 101
        assert self.room_1.get_data()['type'] == 'Single'


class TestOrderDM:
    def setup(self):
        self.room_1 = RoomDM(id=1, price=1000.00, number=101, type='Single')
        self.order_1 = OrderDM(
            id=1,
            check_in_date=datetime.date(year=2020, month=2, day=20),
            check_out_date=datetime.date(year=2020, month=2, day=23),
            order_rooms=[self.room_1, ],
            order_services=[],
        )

    def test_slots(self):
        assert self.order_1.__slots__ == ('_id', '_check_in_date', '_check_out_date', '_order_rooms', '_order_services')

    def test_id_field(self):
        assert isinstance(self.order_1.__fields__['id'], Int) is True
        assert self.order_1.get_data()['id'] == 1

    def test_check_in_date_field(self):
        assert isinstance(self.order_1.__fields__['check_in_date'], Date) is True
        assert self.order_1.get_data()['check_in_date'] == datetime.date(year=2020, month=2, day=20)
        assert str(self.order_1.get_data()['check_in_date']) == '2020-02-20'

    def test_check_out_date_field(self):
        assert isinstance(self.order_1.__fields__['check_out_date'], Date) is True
        assert self.order_1.get_data()['check_out_date'] == datetime.date(year=2020, month=2, day=23)
        assert str(self.order_1.get_data()['check_out_date']) == '2020-02-23'

    def test_order_rooms_field(self):
        assert isinstance(self.order_1.__fields__['order_rooms'], FieldCollection) is True
        assert self.order_1.get_data()['order_rooms'][0]['id'] == 1
        assert self.order_1.get_data()['order_rooms'][0]['price'] == 1000.00
        assert self.order_1.get_data()['order_rooms'][0]['number'] == 101
        assert self.order_1.get_data()['order_rooms'][0]['type'] == 'Single'
        assert self.order_1.get_data()['order_services'] == []

    def test_order_services_field(self):
        assert isinstance(self.order_1.__fields__['order_services'], FieldCollection) is True
