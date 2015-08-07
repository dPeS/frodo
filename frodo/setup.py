from frodo.constants import FRODO_MODULE_DATABASE_PREFIX as PREFIX


class InitDatabaseMixin:
    """
    all queries used for db init should be written here
    """
    def _sql_setup_init_database(self):
        """
        create all: tables, indexes, functions, ...
        """
        cursor = self.current_cursor()

        # CONTAINER
        cursor.execute(("create table "
                        "{}_ea_container"
                        "(id serial primary key)").format(PREFIX))
        # ORDER TYPE
        cursor.execute(("create table {prefix}_ea_type(code int, "
                        "container_id int references "
                        "{prefix}_ea_container(id), "
                        "max_quantity int, "
                        "primary key"
                        "(code, container_id) )").format(prefix=PREFIX))
        # ORDER
        cursor.execute(("create table {prefix}_ea_order(id serial primary key, "
                        "order_duration tstzrange, "
                        "container_id int, "
                        "type_code int, "
                        "foreign key(container_id, type_code) "
                        "references {prefix}_ea_type(container_id, code))"
                        "").format(prefix=PREFIX))

        # TOOLS
        # internal FUNCTION used in constraint
        cursor.execute(("create or replace function "
                        "{prefix}_ea_check_orders_fn(tstzrange, int, int) "
                        "returns bigint as "
                        "$$ "
                        "select (select max_quantity from "
                        "{prefix}_ea_type where "
                        "container_id = $2 and code = $3) "
                        " - count(1) from {prefix}_ea_order where "
                        "not isempty(order_duration * $1) "
                        "and container_id = $2 and type_code = $3"
                        "$$ language sql immutable;").format(prefix=PREFIX))

        # addint constraint (whole magic) to ORDER table
        cursor.execute(("alter table {prefix}_ea_order add CHECK "
                        "({prefix}_ea_check_orders_fn(order_duration, "
                        "container_id, type_code) > 0)").format(prefix=PREFIX))
