import os
import psycopg2


def get_connection_from_env():
    """
    returns psycopg2 connection based on system enviroments settings
    """

    """
    first try to get UNIX socket for current shell user
    """
    connection = psycopg2.connect(
        dbname=os.environ['USER'],
        user=os.environ['USER'],
        port=5432,
        host='/var/run/postgresql'
    )
    return connection
