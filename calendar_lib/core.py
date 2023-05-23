from logging import Logger

from calendar_lib.data_access.dao_factory import DaoFactory
from calendar_lib.use_case.auth_use_case import AuthUseCase


class Core:
    def __init__(self, logger: Logger):
        self._dao_factory = DaoFactory()
        self.logger = logger

    def auth_use_case(self) -> AuthUseCase:
        return AuthUseCase(
            logger=self.logger,
            user_dao=self._dao_factory.user_dao()
        )

    @property
    def dao_factory(self):
        return self._dao_factory
