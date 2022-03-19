import yaml
from typing import List, Dict

# This is an approach using YAML
# Alternatives: INI, JSON
# Interesting ideas: dotenv, Hydra (Facebook)

class ConfigParser:

    DEFAULT_FILE_PATH ='/home/lucas-mateo/Desktop/CODE/learn/fcc-fast-api/config.yaml'

    def __init__(self, path: str = DEFAULT_FILE_PATH) -> None:
        self.config_path = path

    def read_yaml(self) -> Dict[str, str]:
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f)

    def get_env(self):
        return self.read_yaml()["ENVIRONMENT"]

    def get_data(self, paths: List[str]) -> Dict[str, str]:
        data = self.read_yaml()
        for path in paths:
            try:
                data = data[path]
            except KeyError as e:
                print(e)
                raise KeyError(f"{path} does not exist as Key")
        return data


if __name__ == '__main__':
    print(ConfigParser().read_yaml())
    print(ConfigParser().get_data(["DATABASE", "DEV"]))