import contextlib
import sqlite3

from hotel_management.domain_model import DomainModel, Int, String, FieldCollection, Bool, Date, DecimalField
from hotel_management.user import Customer

DB_PATH = 'db.sqlite'
connection = sqlite3.connect(DB_PATH)


@contextlib.contextmanager
def data_conn(db_name):
    try:
        # print('Making connection')
        conn = sqlite3.connect(db_name)
        yield conn  # код из блока with выполнится тут
    except sqlite3.OperationalError as e:
        print(f'We had an error: {e}')
    finally:
        # print('Closing connection')
        conn.close()


def create_db(db_path):
    with data_conn(db_path) as conn:
        with conn:
            cursor = conn.cursor()
            # Создание таблицы 'customer'
            cursor.execute("""CREATE TABLE IF NOT EXISTS customer
                              (id INTEGER,
                              name TEXT,
                              is_loyal INTEGER)
                           """)


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class CustomerMapper:
    """
    Паттерн DATA MAPPER
    Слой преобразования данных
    """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id_):
        statement = 'SELECT id, name FROM customer WHERE id=?'
        self.cursor.execute(statement, (id_, ))
        result = self.cursor.fetchall()
        if result:
            return Customer(*result[0])
        else:
            raise RecordNotFoundException(f'Record with id={id_} not found')

    def insert(self, customer):
        statement = f'INSERT INTO customer (id, name, is_loyal) VALUES (?, ?, ?)'
        self.cursor.execute(statement, (customer.id, customer.name, customer.is_loyal))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, customer):
        statement = f'UPDATE customer SET name=?, is_loyal=? WHERE id=?'
        self.cursor.execute(statement, (customer.name, customer.is_loyal, customer.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, customer):
        statement = f'DELETE FROM customer WHERE id=?'
        self.cursor.execute(statement, (customer.id, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class ItemDM(DomainModel):
    id = Int()
    price = DecimalField()

    __unique_key__ = (id,)


# class RoomDM(ItemDM):
#     number = Int()
#     # type = String()
#
#     __unique_key__ = (number,)


class RoomDM(DomainModel):
    id = Int()
    price = DecimalField()
    number = Int()
    type = String()

    __unique_key__ = (id, number)


class ServiceDM(ItemDM):
    title = String()

    __unique_key__ = (title,)


# class OrderItemDM(DomainModel):
#     id = Int()
#
#     __unique_key__ = (id,)
#
#     item = FieldCollection(ItemDM)


class OrderDM(DomainModel):
    id = Int()
    check_in_date = Date()
    check_out_date = Date()

    __unique_key__ = (id,)

    # order_items = FieldCollection(OrderItemDM)
    order_rooms = FieldCollection(RoomDM)
    order_services = FieldCollection(ServiceDM)
