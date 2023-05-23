import pytest
from dotenv import load_dotenv


@pytest.fixture(autouse=True)
def load_env_variables():
    load_dotenv()
