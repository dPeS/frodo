from frodo import setup
from frodo import select
from frodo import insert
from frodo import delete

class FrodoCtxManager:
    """
    Frodo's default Context Manager
    it leaves connection open
    used in django context and in managed mode
    """
    def __init__(self, db):
        self.db = db
        self.db.current_cursor().execute('SAVEPOINT FRODO')

    def __enter__(self):
        return self.db

    def __exit__(self, type, value, traceback):
        if type:
            self.db.current_cursor().execute('ROLLBACK TO FRODO')
        else:
            self.db.commit()
        self.db.close_cursor()


class Base:
    """
    base for all Frodo interfaces
    """
    def __init__(self, connection):
        """
        :param connection: DB API 2.0 connection
        """
        self.connection = connection
        self.cursor = None

    def get_connection(self):
        """
        returns DB API 2.0 connection object
        """
        return self.connection

    def commit(self):
        """
        do commit() connection
        """
        self.connection.commit()

    def rollback(self):
        """
        do rollback() connection
        """
        self.connection.rollback()

    def close(self):
        """
        do close() connection
        """
        self.connection.close()

    def open_cursor(self):
        """
        open_curosor()
        """
        self.cursor = self.connection.cursor()
        return self.cursor

    def current_cursor(self):
        """
        return opened cursor
        """
        if self.cursor and not self.cursor.closed:
            return self.cursor
        else:
            return self.open_cursor()

    def close_cursor(self):
        """
        close_cursor()
        """
        if self.cursor and not self.cursor.closed:
            self.cursor.close()


class FrodoBasicEngine(Base,
                       setup.InitDatabaseMixin,
                       select.SelectMixin,
                       insert.InsertMixin,
                       delete.DeleteMixin):
    """
    Our all-in-one front object facade
    """
    def setup_frodo_in_database(self):
        """
        should be invoked only once
        every next call on existing structure
        will throw Exception
        """
        self._sql_setup_init_database()

    def create_container(self):
        """
        returns ID of NEW empty container or None if failed
        """
        return self._sql_insert_container()

    def _list_containers(self):
        """
        returns ID list of all containers
        """
        return self._sql_select_container_list_all()

    def _drop_empty_container(self, container_id):
        """
        drops EMPTY container
        returns True if success else False
        """
        return self._sql_delete_container_by_id(container_id)

    def add_type_to_container(self, container_id, type_code, max_quantity):
        """
        create NEW type in container
        returns type_code or None if failed
        """
        if container_id is None:
            container_id = 1
        return self._sql_insert_type(container_id, type_code, max_quantity)

    def _remove_type_without_orders(self, container_id, type_code):
        """
        removes type only if no orders made
        returns True if success else False
        """
        return self._sql_delete_type_by_id(container_id, type_code)

    def _list_container_types(self, container_id):
        """
        lists all types with corresponding quantities for particular container
        returns list of (type_code, quantity)
        """
        return self._sql_select_type_list_all(container_id, type_code)

    def make_order(self, container_id, order_list):
        """
        creates new locks
        :param container_id:
        :param order_list: list of all orders to make
        :type order_list: (type_code, quantity, datetime begin, datetime end)
        :returns: order ID list or None if failed
        """
        if container_id is None:
            container_id = 1
        return self._sql_insert_order(container_id, order_list)

    def cancel_order(self, order_list):
        """
        release locks
        :param order_list: list of IDs
        returns True if success else False
        """
        return self._sql_delete_order(order_list)
