import datetime
from unittest import TestCase

from calendar_lib.data_access.database import Database
from calendar_lib.utils import get_config_secrets


class TestDatabase(TestCase):
    def setUp(self):
        self.config_secrets = get_config_secrets()
        self.database = Database(self.config_secrets['connect_db'], 'calendar_api')

    def test_connect_db(self):
        self.assertIsNotNone(self.database.db)
        self.assertIsInstance(self.database.db.cursor(), self.database.db.cursor().__class__)

    def test_fetch_one(self):
        # test that fetch_one returns the expected data for a given query
        query = "SELECT name FROM migrations LIMIT 1"
        expected_data = {'name': 'groups'}
        result = self.database.fetch_one(query)
        self.assertEqual(result, expected_data)

    def test_fetch_all(self):
        # test that fetch_all returns the expected data for a given query
        query = "SELECT name FROM migrations"
        expected_data = {'name': 'groups'}
        result = self.database.fetch_all(query)
        self.assertIn(expected_data, result)

    def test_migrations_table_exists(self):
        # test that the migrations table exists
        query = "SELECT count(*) FROM information_schema.tables WHERE table_name = 'migrations'"
        result = self.database.fetch_one(query)['count']
        self.assertEqual(result, 1)

    def test_migrations_table_has_data(self):
        # test that the migrations table has data
        query = "SELECT count(*) FROM migrations"
        result = self.database.fetch_one(query)['count']
        self.assertGreater(result, 0)
