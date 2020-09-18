import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config' / 'polls.yaml'


def get_config(path):
    """
    Подгрузка файла конфигурации

    :param path:
    :return:
    """

    with open(path) as f:
        config = yaml.safe_load(f)
    return config


config = get_config(config_path)
