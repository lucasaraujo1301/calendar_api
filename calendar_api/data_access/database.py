import logging

import psycopg2.extras
import psycopg2.extensions


class Database:
    logger = logging.getLogger()

    MAX_RETRIES = 5

    def __init__(self):
        self.connection_string = {}
        self._db_connection = None

    def connect_db(self, connection_string, db_name):
        if self._db_connection is None or getattr(self._db_connection, 'closed', 1) > 0:
            connection = psycopg2.connect(connection_string, cursor_factory=psycopg2.extras.DictCursor)
            connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            psycopg2.extras.register_uuid(conn_or_curs=connection)

            # Store the connection string for reconnect
            self.connection_string[db_name] = connection_string
            self._db_connection = connection
            return connection
        return self._db_connection

    def close_db(self):
        if self._db_connection is not None and getattr(self._db_connection, 'closed') == 0:
            self._db_connection.close()
            self._db_connection = None

    def get_db(self, db_name):
        if self._db_connection is not None and self.connection_string:
            self.logger.warning(f'Reconnect needed for {db_name}')
            return self.connect_db(self.connection_string[db_name], db_name)
