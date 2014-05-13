import os
import psycopg2

def get_connection_from_env():
    """
    returns psycopg2 connection based on system enviroments settings
    """

    """
    first try to get UNIX socket for current shell user
    """
    try:
        user = os.environ['USER']
        dbname = os.environ['USER']
        connection = psycopg2.connect(dbname=dbname, user=user)
        return connection
    except:
        pass

    raise Exception('Could not find any route to database, pls check: ')
