from typing import Union, List

from calendar_lib.data_access.database import Database
from calendar_lib.data_classes.user import (
    User,
    UserLogin,
    CreateUserRequest
)


class UserDao(Database):
    def __init__(self, connection_string, db_name):
        super().__init__(connection_string, db_name)

    def create_user(self, user: CreateUserRequest) -> None:
        sql = """INSERT INTO users (name, cpf, email, password, group_uuid)
                 VALUES (%s, %s, %s, %s, %s);"""

        self.execute(sql, user.name, user.cpf, user.email, user.generate_password_hash(), user.group_uuid)
        return

    def get_all_users(self) -> List[User]:
        sql = """SELECT users.uuid,
                        users.name,
                        users.cpf,
                        users.email,
                        users.active,
                        groups.name AS group_name
                 FROM users
                 LEFT JOIN groups USING (uuid);"""
        result = self.fetch_all(sql)

        return [User(**r) for r in result]

    def get_user_by_email(self, username: str, with_password: bool = False) -> Union[UserLogin, None]:
        sql = f"""SELECT users.uuid,
                        users.name,
                        users.cpf,
                        users.email,
                        users.active,
                        {'users.password,' if with_password else ''}
                        groups.name AS group_name
                  FROM users
                  LEFT JOIN groups USING (uuid)
                  WHERE users.email = %s;"""
        result = self.fetch_one(sql, username)

        return UserLogin(**result) if result else None

    def get_user_by_cpf(self, user_cpf: str) -> Union[UserLogin, None]:
        sql = """SELECT users.uuid,
                        users.name,
                        users.cpf,
                        users.email,
                        users.active,
                        groups.name AS group_name
                 FROM users
                 LEFT JOIN groups USING (uuid)
                 WHERE users.cpf = %s;"""

        result = self.fetch_one(sql, user_cpf)
        return User(**result) if result else None
