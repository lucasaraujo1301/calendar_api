from calendar_lib.data_access.user_dao import UserDao
from calendar_lib.utils import get_config_secrets


class DaoFactory:
    def __init__(self):
        self._connection_string = get_config_secrets()['connect_db']
        self._db_name = "calendar_api"

    def user_dao(self) -> UserDao:
        return UserDao(self._connection_string, self._db_name)
