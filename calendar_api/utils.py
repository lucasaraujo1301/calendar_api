import os
import yaml

from yaml.loader import SafeLoader

path = os.path.dirname(__file__)


def get_config_secrets():
    with open(os.path.join(path, 'config/local_config.yaml'), 'r') as f:
        return yaml.load(f, Loader=SafeLoader)
