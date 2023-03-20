import os
import yaml

from yaml.loader import SafeLoader

path = os.path.dirname(__file__)


def get_config_secrets():
    config_file = os.getenv('ENVIRONMENT_CONFIG', 'local_config')
    with open(os.path.join(path, f'config/{config_file}.yaml'), 'r') as f:
        return yaml.load(f, Loader=SafeLoader)
