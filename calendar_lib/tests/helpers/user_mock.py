from uuid import uuid4
from calendar_lib.data_classes.user import UserLogin, GroupEnum
from flask_bcrypt import generate_password_hash


def create_mock_user(name='Test User', cpf='12345678900', email='test@test.com', group=GroupEnum.user, active=True,
                     password='password'):
    return UserLogin(
        uuid=uuid4(),
        name=name,
        cpf=cpf,
        email=email,
        group_name=group,
        active=active,
        password=generate_password_hash(password)
    )


def create_mock_user_inactive(name='Test User', cpf='12345678900', email='test@test.com', group=GroupEnum.user,
                              active=False, password='password'):
    return UserLogin(
        uuid=uuid4(),
        name=name,
        cpf=cpf,
        email=email,
        group_name=group,
        active=active,
        password=generate_password_hash(password)
    )
