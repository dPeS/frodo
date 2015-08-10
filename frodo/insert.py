import datetime

from frodo.constants import FRODO_MODULE_DATABASE_PREFIX as PREFIX
from frodo.constants import DEFAULT_ORDER_TIMEOUT as TIMEOUT
import psycopg2.extras


class InsertMixin:
    """
    all insert queries should be written here
    """
    def _sql_insert_container(self):
        """
        creates new cointainer
        """
        cursor = self.current_cursor()
        cursor.execute(
            "insert into {}_ea_container "
            "values(default)"
            "returning id".format(PREFIX)
        )
        return cursor.fetchone()

    def _sql_insert_type(self, container_id, type_code, max_quantity):
        """
        creates new type for container
        """
        cursor = self.current_cursor()
        cursor.execute(
            "insert into {}_ea_type("
            "container_id, code, max_quantity) "
            "values(%s, %s, %s)".format(PREFIX),
            (container_id, type_code, max_quantity)
        )

    def _sql_insert_order(self, container_id, order_list):
        """
        creates new order
        """
        cursor = self.current_cursor()
        for type_code, quantity, begin, end in order_list:
            for cycle in xrange(quantity):
                cursor.execute(
                    "insert into {}_ea_order("
                    "container_id, "
                    "type_code, "
                    "order_duration, "
                    "order_timeout) "
                    "values(%s, %s, %s, now() + %s)".format(PREFIX),
                    (
                        container_id,
                        type_code,
                        psycopg2.extras.DateTimeTZRange(begin, end, '[]'),
                        datetime.timedelta(seconds=TIMEOUT),
                    )
                )
