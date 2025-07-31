import pytest
from dagfactory._yaml import load_yaml_file
from dagfactory.utils import update_yaml_structure
from pathlib import Path


@pytest.fixture
def read_dataset_yaml():
    here = Path(__file__).parent.resolve()
    def _read(file_name):
        file_path = f"{here}/mocks/datasets/{file_name}" 
        _yaml = load_yaml_file(file_path)
        return update_yaml_structure(_yaml)
    return _read