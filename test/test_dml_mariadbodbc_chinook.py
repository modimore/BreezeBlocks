import os
import pyodbc
import unittest
from breezeblocks import Database

from base_dml_chinook_tests import BaseDMLChinookTests

CONNECTION_STRING = "DSN=Chinook_MariaDB"

class MariaDBODBCTests(BaseDMLChinookTests, unittest.TestCase):
    """Tests using MariaDB through an ODBC adapter."""
    
    def setUp(self):
        self.db = Database(dsn=CONNECTION_STRING, dbapi_module=pyodbc)
