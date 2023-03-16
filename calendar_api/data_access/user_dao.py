from typing import Optional

from calendar_api.data_access.database import Database
from calendar_api.data_classes.user import User


class UserDao(Database):
    def __init__(self, connection_string, db_name):
        super().__init__(connection_string, db_name)

    def get_user_by_username(self, username: str) -> Optional[User]:
        sql = """SELECT name,
                        cpf,
                        email,
                        active
                 FROM users 
                 WHERE email = %s;"""
        result = self.fetch_one(sql, username)

        return User(**result) if result else None
