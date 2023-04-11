import logging
from typing import Dict, List

import psycopg2.extras
import psycopg2.extensions


class Database:
    def __init__(self, connection_string: str, db_name: str):
        self.logger = logging.getLogger()
        self.MAX_RETRIES = 5
        self.connection_string = {}
        self._db_name = db_name
        self._db = self.connect_db(connection_string)

    def connect_db(self, connection_string):
        self.logger.info('Connecting the database.')
        connection = psycopg2.connect(connection_string, cursor_factory=psycopg2.extras.DictCursor)
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        psycopg2.extras.register_uuid(conn_or_curs=connection)

        # Store the connection string for reconnect
        self.connection_string[self._db_name] = connection_string
        return connection

    def close_db(self):
        if self._db and getattr(self._db, 'closed') == 0:
            self.logger.info('Closing the database.')
            self._db.close()

    def get_db(self):
        if self._db is None or (self.connection_string and getattr(self._db, 'closed') > 0):
            self.logger.warning(f'Reconnect needed for {self._db_name}.')
            return self.connect_db(self.connection_string[self._db_name])
        return self._db

    def fetch_one(self, sql, *args) -> Dict:
        if getattr(self._db, 'closed') > 0:
            self._db = self.get_db()
        with self._db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            transaction_fails = 0
            while True:
                try:
                    cur.execute(sql, args)
                    query_result = cur.fetchone()
                    self._db.commit()
                    self.logger.info('Closing the database after completing the query.')
                    self.close_db()
                    return query_result
                except psycopg2.extensions.TransactionRollbackError:
                    self.logger.warning('Transaction Error Rollback triggered')
                    self._db.rollbak()
                    transaction_fails += 1
                    if transaction_fails > self.MAX_RETRIES:
                        raise
                except Exception:
                    self.logger.warning('Rollback triggered')
                    self._db.rollback()
                    raise

    def fetch_all(self, sql, *args) -> List[Dict]:
        if getattr(self._db, 'closed') > 0:
            self._db = self.get_db()
        with self._db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            transaction_fails = 0
            while True:
                try:
                    cur.execute(sql, args)
                    query_result = cur.fetchall()
                    self._db.commit()
                    self.logger.info('Closing the database after completing the query.')
                    self.close_db()
                    return query_result
                except psycopg2.extensions.TransactionRollbackError:
                    self.logger.warning('Transaction Error Rollback triggered')
                    self._db.rollbak()
                    transaction_fails += 1
                    if transaction_fails > self.MAX_RETRIES:
                        raise
                except Exception:
                    self.logger.warning('Rollback triggered')
                    self._db.rollback()
                    raise

    def execute(self, sql: str, *args) -> None:
        """Function to INSERT data to database."""
        if getattr(self._db, 'closed') > 0:
            self._db = self.get_db()
        with self._db.cursor() as cur:
            transaction_fails = 0
            while True:
                try:
                    cur.execute(sql, args)
                    self._db.commit()
                    self.logger.info('Closing the database after completing the query.')
                    self.close_db()
                    break
                except psycopg2.extensions.TransactionRollbackError:
                    self.logger.warning('Transaction Error Rollback triggered')
                    self._db.rollbak()
                    transaction_fails += 1
                    if transaction_fails > self.MAX_RETRIES:
                        raise
                except Exception:
                    self.logger.warning('Rollback triggered')
                    self._db.rollback()
                    raise
