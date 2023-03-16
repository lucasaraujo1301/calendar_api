from calendar_api.data_access.dao_factory import DaoFactory


class Core:
    def __init__(self):
        self._dao_factory = DaoFactory()
