from dataclasses import dataclass
from uuid import UUID

from flask_bcrypt import check_password_hash, generate_password_hash


@dataclass
class User:
    uuid: UUID
    name: str
    cpf: str
    email: str
    active: bool
    group_name: str


@dataclass
class UserLogin(User):
    password: UUID

    def validate_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


@dataclass
class UserLoginRequest:
    username: str
    password: str


@dataclass
class CreateUserRequest:
    name: str
    cpf: str
    email: str
    group_uuid: UUID
    password: str

    def generate_password_hash(self):
        return generate_password_hash(self.password, 10)
