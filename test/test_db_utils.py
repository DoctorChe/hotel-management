import os
import sqlite3

import pytest

from hotel_management.db_utils import create_db, CustomerMapper, RecordNotFoundException, DbUpdateException
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
