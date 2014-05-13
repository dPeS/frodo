"""
typical client has to use only ONE of those interfaces
"""

from frodo.abstraction import FrodoBasicEngine, FrodoCtxManager
from frodo import utils

def plain():
    """
    plain interface
    You have to manage exeptions, commits and rollbacks by yourself
    """
    connection = utils.get_connection_from_env()
    return FrodoBasicEngine(connection)

def managed():
    """
    managed interface
    returns context manager
    """
    connection = utils.get_connection_from_env()
    return FrodoCtxManager( FrodoBasicEngine(connection) )

def django():
    """
    returns obj wrapper for all API calls
    prepared to use inside Django view
    returns context manager
    example use:
        with frodo.django() as db:
            db.setup_frodo_in_database()
    """
    from django.db import connection
    return FrodoCtxManager( FrodoBasicEngine(connection) )
