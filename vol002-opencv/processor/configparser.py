from pathlib import Path
import yaml

config_path = Path(__file__).parent / '../config.yml'


def load():
    with config_path.open() as f:
        config = yaml.load(f)

    return config


def save(config):
    with config_path.open('w') as f:
        yaml.dump(config, f)
