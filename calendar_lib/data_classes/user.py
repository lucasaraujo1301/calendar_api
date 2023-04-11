from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import UUID

from flask_bcrypt import check_password_hash, generate_password_hash


class GroupEnum(Enum):
    admin = 'Admin'
    user = 'User'


@dataclass
class User:
    uuid: UUID
    name: str
    cpf: str
    email: str
    active: bool
    group_name: GroupEnum


@dataclass
class UserLogin(User):
    password: Optional[str] = None

    def validate_password(self, password: str) -> bool:
        if not self.password:
            return False
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
        return generate_password_hash(self.password)
