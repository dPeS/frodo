import unittest
import datetime

import frodo
from frodo.constants import FRODO_MODULE_DATABASE_PREFIX as PREFIX

class BasicTestCase(unittest.TestCase):
    """
    Simple usage tests
    in plain mode
    """
    def setUp(self):
        self.db = frodo.plain()
        cursor = self.db.current_cursor()

        # clean up db
        try:
            cursor.execute("drop table {}_ea_container CASCADE".format(PREFIX))
            cursor.execute("drop table {}_ea_type CASCADE".format(PREFIX))
            cursor.execute("drop table {}_ea_order CASCADE".format(PREFIX))
            self.db.commit()
        except:
            self.db.rollback()

        self.db.setup_frodo_in_database()
        self.db.commit()

    def tearDown(self):
        '''
        '''

    def test_999(self):
        """
        add new container
        """
        self.db.create_container()
        self.db.commit()
        self.assertTrue(True)

    def test_998(self):
        """
        add type
        """
        self.db.create_container()
        self.db.add_type_to_container(None, 10, 1)
        self.db.commit()
        self.assertTrue(True)

    def test_997(self):
        """
        make order
        """
        self.db.create_container()
        self.db.add_type_to_container(None, 10, 1)
        self.db.make_order(None, [(10, 1, datetime.datetime(2010,1,1),
                                   datetime.datetime(2010,1,2))])
        self.db.commit()
        self.assertTrue(True)

    def test_996(self):
        """
        make 2 orders in the same time
        """
        self.db.create_container()
        self.db.add_type_to_container(None, 10, 1)
        self.db.add_type_to_container(None, 20, 1)
        self.db.make_order(None, [(10, 1, datetime.datetime(2010,1,1),
                                   datetime.datetime(2010,1,2))])
        self.db.make_order(None, [(20, 1, datetime.datetime(2010,1,1),
                                   datetime.datetime(2010,1,2))])
        self.db.commit()
        self.assertTrue(True)

    def test_995(self):
        """
        make order bigger then resources in 1 call
        """
        self.db.create_container()
        self.db.add_type_to_container(None, 10, 1)
        with self.assertRaises(Exception):
            self.db.make_order(None, [(10, 2, datetime.datetime(2010,1,1),
                                    datetime.datetime(2010,1,2))])

    def test_994(self):
        """
        make order bigger then resources in 2 calls
        """
        self.db.create_container()
        self.db.add_type_to_container(None, 10, 2)
        self.db.make_order(None, [(10, 2, datetime.datetime(2010,1,1),
                                datetime.datetime(2010,1,2))])
        with self.assertRaises(Exception):
            self.db.make_order(None, [(10, 1, datetime.datetime(2010,1,1),
                                    datetime.datetime(2010,1,2))])

if __name__ == '__main__':
    unittest.main()
