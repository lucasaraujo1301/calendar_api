import os
import yaml

from yaml.loader import SafeLoader

path = os.path.dirname(__file__)


def get_config_secrets():
    config_file = os.environ['ENVIRONMENT_CONFIG']
    with open(os.path.join(path, f'config/{config_file}.yaml'), 'r') as f:
        return yaml.load(f, Loader=SafeLoader)
