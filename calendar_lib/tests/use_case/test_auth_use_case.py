import uuid
from unittest import TestCase
from unittest.mock import patch, MagicMock

import pytest

from calendar_api import Core
from calendar_lib.data_classes.user import UserLoginRequest, CreateUserRequest
from calendar_lib.tests.helpers.user_mock import create_mock_user, create_mock_user_inactive


class TestAuthUseCase(TestCase):
    core = Core()

    @classmethod
    def setUp(cls):
        cls.auth_use_case = cls.core.auth_use_case()
        cls.user_dao = cls.core._dao_factory.user_dao()

    @classmethod
    def tearDownClass(cls):
        user_created = create_mock_user()
        query = "DELETE FROM users WHERE email = %s;"
        cls.core._dao_factory.user_dao().execute(query, user_created.email)

    def test_login_user_doesnt_exist(self):
        # User doesn't exist
        payload = UserLoginRequest(username='test@test.com', password='password')
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

    @patch('calendar_lib.data_access.user_dao.UserDao.get_user_by_email')
    def test_login_inactive_user(self, mock_get_user):
        # Inactive user
        mock_user = create_mock_user_inactive()
        mock_get_user.return_value = mock_user

        payload = UserLoginRequest(username=mock_user.email, password='password')
        with pytest.raises(Exception, match='User is not active.'):
            self.auth_use_case.login(payload)

    @patch('calendar_lib.data_access.user_dao.UserDao.get_user_by_cpf')
    @patch('calendar_lib.data_access.user_dao.UserDao.get_user_by_email')
    def test_register(self, mock_get_user_by_email, mock_get_user_by_cpf):
        # Getting the group_uuid existent
        query = "SELECT uuid FROM groups LIMIT 1"
        group = self.user_dao.fetch_one(query)

        # Creating
        user_request = CreateUserRequest(
            name='Test User',
            cpf='12345678900',
            email='test@test.com',
            password='password123',
            group_uuid=group['uuid']
        )

        mock_get_user_by_cpf.return_value = None
        mock_get_user_by_email.return_value = None

        # Call register method and check return value
        user, errors = self.auth_use_case.register(user_request)
        assert user is None
        assert errors is None

        mock_get_user_by_cpf.return_value = user_request
        mock_get_user_by_email.return_value = None

        # Call register method and check return value
        user, errors = self.auth_use_case.register(user_request)
        assert user is None
        assert errors == [{'cpf': 'CPF already exist.'}]

        mock_get_user_by_cpf.return_value = None
        mock_get_user_by_email.return_value = user_request

        # Call register method and check return value
        user, errors = self.auth_use_case.register(user_request)
        assert user is None
        assert errors == [{'email': 'Email already exist.'}]
