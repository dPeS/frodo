from frodo.constants import FRODO_MODULE_DATABASE_PREFIX as PREFIX

class DeleteMixin:
    """
    all delete queries should be written here
    """
    def _sql_delete_order(self, order_list):
        """
        delete
        :order_list: list of IDs (ints)
        """
        cursor = self.current_cursor()
        args_str = ','.join(cursor.mogrify("%s", (x, )) for x in order_list)
        cursor.execute("delete from {}_ea_order where id in ({})".format(PREFIX, args_str))
