import os
from typing import Tuple


def get_db_configs() -> Tuple[str, str]:
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_port = os.getenv('DB_PORT')
    db_connect_timeout = os.getenv('DB_CONNECT_TIMEOUT')

    # Split the string_connect due max line length exceeded
    string_connect = f'host={db_host} dbname={db_name} user={db_user} password={db_password} port={db_port}'
    string_connect += f' connect_timeout={db_connect_timeout}'
    return string_connect, db_name
