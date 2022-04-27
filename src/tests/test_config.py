import pytest

from app.utils.config import ConfigParser

def test_validation_yaml():
    with pytest.raises(FileNotFoundError):
        parser = ConfigParser(path='path/to/inexistent_file.yaml')
        parser.read_yaml()


