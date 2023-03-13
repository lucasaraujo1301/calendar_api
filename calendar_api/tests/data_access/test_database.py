from unittest import TestCase

from calendar_api.data_access.database import Database
from calendar_api.utils import get_config_secrets


class TestDatabase(TestCase):
    def setUp(self):
        self.db = Database()
        self.config_secrets = get_config_secrets()

    def test_connect_db(self):
        assert self.db.connect_db(self.config_secrets['connect_db'], 'calendar_api') is not None
        assert self.db.connection_string is not {}
        assert self.db._db_connection is not None

    def test_close_db(self):
        self.db.connect_db(self.config_secrets['connect_db'], 'calendar_api')
        self.db.close_db()
        assert self.db._db_connection is None

    def test_get_db(self):
        assert self.db.get_db('calendar_api') is None

        # Testing with a open database
        self.db.connect_db(self.config_secrets['connect_db'], 'calendar_api')
        assert self.db.get_db('calendar_api') is not None
        assert self.db.connection_string
        assert self.db._db_connection is not None
