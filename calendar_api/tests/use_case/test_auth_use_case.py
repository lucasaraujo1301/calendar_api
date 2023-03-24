from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4

import pytest
from flask_bcrypt import generate_password_hash

from calendar_api import Core
from calendar_api.data_classes.user import UserLoginRequest, UserLogin


class TestAuthUseCase(TestCase):
    def setUp(self):
        self.auth_use_case = Core().auth_use_case()
        self.user_dao = Core()._dao_factory.user_dao()

    @patch('calendar_api.data_access.user_dao.UserDao.get_user_by_email_with_password')
    def test_login(self, get_user_by_email_with_password):
        get_user_by_email_with_password.return_value = None

        # User doesn't exist
        payload = UserLoginRequest(username='test@test.com', password='test123')
        with pytest.raises(Exception, match="User doesn't exist."):
            self.auth_use_case.login(payload)

        get_user_by_email_with_password.return_value = UserLogin(
            uuid=uuid4(),
            name='Test',
            cpf='12345678910',
            email='admin@admin.com',
            group_name='Admin',
            active=True,
            password=generate_password_hash('admin123', 10)
        )
        # Wrong password
        payload = UserLoginRequest(username='admin@admin.com', password='test123')
        with pytest.raises(Exception, match='Password is wrong.'):
            self.auth_use_case.login(payload)

        # Success case
        payload = UserLoginRequest(username='admin@admin.com', password='admin123')
        user = self.user_dao.get_user_by_email_with_password(payload.username)
        request = self.auth_use_case.login(payload)
        assert request is not None
        assert request == user.uuid
