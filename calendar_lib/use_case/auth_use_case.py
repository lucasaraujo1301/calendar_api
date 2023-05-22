from logging import Logger
from typing import List, Dict, Union, Tuple

from calendar_lib.data_access.user_dao import UserDao
from calendar_lib.data_classes.user import UserLoginRequest, CreateUserRequest, User
from calendar_lib.exceptions.user_exceptions import UserNotFoundError, PasswordInvalidError


class AuthUseCase:
    def __init__(self, logger: Logger, user_dao: UserDao):
        self.logger = logger
        self._dao = user_dao

    def login(self, user_request: UserLoginRequest) -> User:
        self.logger.info('Getting the user with password column')
        user = self._dao.get_user_by_email(user_request.username, True)

        self.logger.info(f'Debugging user: {user}')
        if not user:
            self.logger.warning("User doesn't exist.")
            raise UserNotFoundError("User doesn't exist.")

        if not user.validate_password(user_request.password):
            self.logger.warning('Password is wrong.')
            raise PasswordInvalidError('Password is wrong.')

        if not user.active:
            self.logger.warning('User is not active.')
            raise UserNotFoundError('User is not active.')

        return user

    def register(self, user_request: CreateUserRequest) -> Union[Tuple[None, List[Dict]], Tuple[None, None]]:
        errors = []
        if self._dao.get_user_by_cpf(user_request.cpf) is not None:
            self.logger.warning('CPF already exist.')
            errors.append({'cpf': 'CPF already exist.'})
        if self._dao.get_user_by_email(user_request.email) is not None:
            self.logger.warning('Email already exist.')
            errors.append({'email': 'Email already exist.'})
        if errors:
            return None, errors

        try:
            return self._dao.create_user(user_request), None
        except Exception as e:
            self.logger.warning('Something goes wrong: ', e)
            raise
