import logging
from typing import Dict, List

import psycopg2.extras
import psycopg2.extensions


class Database:
    MAX_RETRIES = 5

    def __init__(self, connection_string: str, db_name: str):
        self.logger = logging.getLogger()
        self._db_name = db_name
        self.connection_string = connection_string
        self._db = None

    @property
    def db(self):
        if self._db is None or self._db.closed > 0:
            self.logger.warning(f"Reconnecting to database '{self._db_name}'.")
            self._db = psycopg2.connect(self.connection_string, cursor_factory=psycopg2.extras.RealDictCursor)
            self._db.set_session(autocommit=True)
        return self._db

    def fetch_one(self, sql: str, *args) -> Dict:
        with self.db.cursor() as cur:
            transaction_fails = 0
            while True:
                try:
                    cur.execute(sql, args)
                    query_result = cur.fetchone()
                    self.logger.info('Query completed successfully.')
                    return query_result
                except psycopg2.extensions.TransactionRollbackError:
                    self.logger.exception('Transaction rollback triggered.')
                    self.db.rollback()
                    transaction_fails += 1
                    if transaction_fails > self.MAX_RETRIES:
                        raise
                except Exception:
                    self.logger.exception('Error occurred during query execution.')
                    self.db.rollback()
                    raise

    def fetch_all(self, sql: str, *args) -> List[Dict]:
        with self.db.cursor() as cur:
            transaction_fails = 0
            while True:
                try:
                    cur.execute(sql, args)
                    query_result = cur.fetchall()
                    self.logger.info('Query completed successfully.')
                    return query_result
                except psycopg2.extensions.TransactionRollbackError:
                    self.logger.exception('Transaction rollback triggered.')
                    self.db.rollback()
                    transaction_fails += 1
                    if transaction_fails > self.MAX_RETRIES:
                        raise
                except Exception:
                    self.logger.exception('Error occurred during query execution.')
                    self.db.rollback()
                    raise

    def execute(self, sql: str, *args) -> None:
        """Function to INSERT data to database."""
        with self.db.cursor() as cur:
            transaction_fails = 0
            while True:
                try:
                    cur.execute(sql, args)
                    self.logger.info('Query completed successfully.')
                    break
                except psycopg2.extensions.TransactionRollbackError:
                    self.logger.exception('Transaction rollback triggered.')
                    self.db.rollback()
                    transaction_fails += 1
                    if transaction_fails > self.MAX_RETRIES:
                        raise
                except Exception:
                    self.logger.exception('Error occurred during query execution.')
                    self.db.rollback()
                    raise
