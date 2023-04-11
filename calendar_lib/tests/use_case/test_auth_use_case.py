from unittest import TestCase
from unittest.mock import patch

import pytest

from calendar_api import Core
from calendar_lib.data_classes.user import UserLoginRequest
from calendar_lib.tests.helpers.user_mock import create_mock_user


class TestAuthUseCase(TestCase):
    def setUp(self):
        self.auth_use_case = Core().auth_use_case()
        self.user_dao = Core()._dao_factory.user_dao()

    def test_login_user_doesnt_exist(self):
        # User doesn't exist
        payload = UserLoginRequest(username='test@test.com', password='test123')
        with pytest.raises(Exception, match="User doesn't exist."):
            self.auth_use_case.login(payload)

    @patch('calendar_lib.data_access.user_dao.UserDao.get_user_by_email')
    def test_login_wrong_password(self, mock_get_user):
        # Wrong password
        mock_get_user.return_value = create_mock_user()
        payload = UserLoginRequest(username='admin@admin.com', password='test123')
        with pytest.raises(Exception, match='Password is wrong.'):
            self.auth_use_case.login(payload)

    @patch('calendar_lib.data_access.user_dao.UserDao.get_user_by_email')
    def test_login_success(self, mock_get_user):
        mock_user = create_mock_user()
        mock_get_user.return_value = mock_user

        # Login with correct credentials
        payload = UserLoginRequest(username=mock_user.email, password='password')
        request = self.auth_use_case.login(payload)
        assert request is not None
        assert request.uuid == mock_user.uuid
