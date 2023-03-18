from typing import Union, List

from calendar_api.data_access.database import Database
from calendar_api.data_classes.user import User, UserLogin


class UserDao(Database):
    def __init__(self, connection_string, db_name):
        super().__init__(connection_string, db_name)

    def get_all_users(self) -> List[User]:
        sql = """SELECT users.uuid,
                        users.name,
                        users.cpf,
                        users.email,
                        users.active,
                        users.password,
                        groups.name as group_name
                 FROM users
                 LEFT JOIN groups on groups.uuid = users.group_uuid;"""
        result = self.fetch_all(sql)

        return [User(**r) for r in result]

    def get_user_by_username_with_password(self, username: str) -> Union[UserLogin, None]:
        sql = """SELECT users.uuid,
                        users.name,
                        users.cpf,
                        users.email,
                        users.active,
                        users.password,
                        groups.name as group_name
                 FROM users
                 LEFT JOIN groups on groups.uuid = users.group_uuid
                 WHERE users.email = %s;"""
        result = self.fetch_one(sql, username)

        return UserLogin(**result) if result else None
