from unittest import TestCase

from calendar_lib.data_access.database import Database
from calendar_lib.utils import get_config_secrets


class TestDatabase(TestCase):
    def setUp(self):
        self.config_secrets = get_config_secrets()
        self.db = Database(self.config_secrets['connect_db'], 'calendar_api')

    def test_connect_db(self):
        assert self.db.connect_db(self.config_secrets['connect_db']) is not None
        assert self.db.connection_string is not {}
        assert self.db._db is not None

    def test_close_db(self):
        self.db.connect_db(self.config_secrets['connect_db'])
        self.db.close_db()
        assert getattr(self.db._db, 'closed') > 0

    def test_get_db(self):
        # Testing with a open database
        self.db.connect_db(self.config_secrets['connect_db'])
        assert self.db.get_db() is not None
        assert self.db.connection_string
        assert self.db._db is not None
