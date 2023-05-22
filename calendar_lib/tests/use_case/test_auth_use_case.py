from unittest import TestCase

import pytest
from mockito import mock, when

from calendar_api import Core
from calendar_lib.data_classes.user import UserLoginRequest, CreateUserRequest
from calendar_lib.tests.helpers.user_mock import create_mock_user, create_mock_user_inactive


class TestAuthUseCase(TestCase):
    core = Core()
    user_dao = core.dao_factory.user_dao()

    def setUp(self):
        self.auth_use_case = self.core.auth_use_case()
        self.mock_user_return = create_mock_user()
        self.mock_user_dao = mock(self.user_dao)

    @classmethod
    def tearDownClass(cls):
        """
        Method to delete the user created by the tests and close the database connection
        :return: None
        """
        user_created = create_mock_user()
        query = "DELETE FROM users WHERE email = %s;"
        cls.user_dao.execute(query, user_created.email)
        cls.user_dao._db.close()

        assert cls.user_dao._db.closed > 0

    def test_login_user_doesnt_exist(self):
        # User doesn't exist
        payload = UserLoginRequest(username='test@test.com', password='password')
        with pytest.raises(Exception, match="User doesn't exist."):
            self.auth_use_case.login(payload)

    def test_login_wrong_password(self):
        # Mock user_dao.get_user_by_email method
        when(self.mock_user_dao).get_user_by_email('test@test.com', True).thenReturn(self.mock_user_return)

        # Inject the mock user_dao into the auth_use_case instance
        self.auth_use_case._dao = self.mock_user_dao

        # Wrong password
        payload = UserLoginRequest(username='test@test.com', password='test123')
        with pytest.raises(Exception, match='Password is wrong.'):
            self.auth_use_case.login(payload)

    def test_login_success(self):
        # Mock user_dao.get_user_by_email method
        when(self.mock_user_dao).get_user_by_email('test@test.com', True).thenReturn(self.mock_user_return)

        # Inject the mock user_dao into the auth_use_case instance
        self.auth_use_case._dao = self.mock_user_dao

        # Login with correct credentials
        payload = UserLoginRequest(username=self.mock_user_return.email, password='password')
        request = self.auth_use_case.login(payload)
        assert request is not None
        assert request.uuid == self.mock_user_return.uuid

    def test_login_inactive_user(self):
        # Inactive user
        mock_user = create_mock_user_inactive()

        # Mock user_dao.get_user_by_email method
        when(self.mock_user_dao).get_user_by_email('test@test.com', True).thenReturn(mock_user)

        # Inject the mock user_dao into the auth_use_case instance
        self.auth_use_case._dao = self.mock_user_dao

        payload = UserLoginRequest(username=mock_user.email, password='password')
        with pytest.raises(Exception, match='User is not active.'):
            self.auth_use_case.login(payload)

    def test_register(self):
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

        # Call register method and check return value
        user, errors = self.auth_use_case.register(user_request)
        assert user is None
        assert errors is None

        # Inject the mock user_dao into the auth_use_case instance
        self.auth_use_case._dao = self.mock_user_dao

        # Mock user_dao.get_user_by_cpf method
        when(self.mock_user_dao).get_user_by_cpf(user_request.cpf).thenReturn(user_request)
        when(self.mock_user_dao).get_user_by_email(user_request.email).thenReturn(None)

        # Call register method and check return value
        user, errors = self.auth_use_case.register(user_request)
        assert user is None
        assert errors == [{'cpf': 'CPF already exist.'}]

        # Mock user_dao.get_user_by_email and user_dao.get_user_by_cpf methods
        when(self.mock_user_dao).get_user_by_cpf(user_request.cpf).thenReturn(None)
        when(self.mock_user_dao).get_user_by_email(user_request.email).thenReturn(user_request)

        # Call register method and check return value
        user, errors = self.auth_use_case.register(user_request)
        assert user is None
        assert errors == [{'email': 'Email already exist.'}]
