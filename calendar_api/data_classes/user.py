from dataclasses import dataclass


@dataclass
class User:
    name: str
    cpf: str
    email: str
    active: bool

