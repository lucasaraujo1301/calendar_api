from logging import Logger
from uuid import UUID

from calendar_api.data_access.user_dao import UserDao
from calendar_api.data_classes.user import UserLoginRequest


class AuthUseCase:
    def __init__(self, logger: Logger, user_dao: UserDao):
        self.logger = logger
        self._dao = user_dao

    def login(self, user_request: UserLoginRequest) -> UUID:
        user = self._dao.get_user_by_username_with_password(user_request.username)

        if not user:
            self.logger.warning("User doesn't exist.")
            raise Exception("User doesn't exist.")

        if user.validate_password(user_request.password) and user.active:
            return user.uuid

        self.logger.warning('Password is wrong.')
        raise Exception('Password is wrong.')
