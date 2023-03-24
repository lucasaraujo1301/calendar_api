from logging import Logger
from typing import List, Dict, Union, Tuple
from uuid import UUID

from calendar_lib.data_access.user_dao import UserDao
from calendar_lib.data_classes.user import UserLoginRequest, CreateUserRequest


class AuthUseCase:
    def __init__(self, logger: Logger, user_dao: UserDao):
        self.logger = logger
        self._dao = user_dao

    def login(self, user_request: UserLoginRequest) -> UUID:
        user = self._dao.get_user_by_email_with_password(user_request.username)

        if not user:
            self.logger.warning("User doesn't exist.")
            raise Exception("User doesn't exist.")

        if user.validate_password(user_request.password) and user.active:
            return user.uuid

        self.logger.warning('Password is wrong.')
        raise Exception('Password is wrong.')

    def register(self, user_request: CreateUserRequest) -> Union[Tuple[None, List[Dict]], Tuple[None, None]]:
        errors = []
        if self._dao.get_user_by_cpf(user_request.cpf):
            errors.append({'cpf': 'CPF already exist.'})
        if self._dao.get_user_by_email_with_password(user_request.email):
            errors.append({'email': 'Email already exist.'})
        if errors:
            return None, errors

        try:
            return self._dao.create_user(user_request), None
        except Exception as e:
            self.logger.warning('Something goes wrong: ', e)
            raise