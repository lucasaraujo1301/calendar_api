from calendar_lib.data_access.user_dao import UserDao
from calendar_lib.utils import get_db_configs


class DaoFactory:
    def __init__(self):
        self._connection_string, self._db_name = get_db_configs()

    def user_dao(self) -> UserDao:
        return UserDao(self._connection_string, self._db_name)
