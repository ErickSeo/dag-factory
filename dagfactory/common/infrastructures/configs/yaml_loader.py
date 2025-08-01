from pathlib import Path
from typing import Mapping, Any
import yaml, os

from dagfactory.common.ports import IConfigLoader
from dagfactory.common.infrastructures.serializers.dynamic_cast import cast_with_type

def _join(loader: yaml.FullLoader, node: yaml.Node) -> str:
    return "".join(str(i) for i in loader.construct_sequence(node))

def _or(loader: yaml.FullLoader, node: yaml.Node) -> str:
    return " | ".join(f"({i})" for i in loader.construct_sequence(node))

def _and(loader: yaml.FullLoader, node: yaml.Node) -> str:
    return " & ".join(f"({i})" for i in loader.construct_sequence(node))

yaml.add_constructor("!join", _join, yaml.FullLoader)
yaml.add_constructor("!or", _or, yaml.FullLoader)
yaml.add_constructor("!and", _and, yaml.FullLoader)


class YamlConfigLoader(IConfigLoader):
    def load(self, path: str) -> Mapping[str, Any]:
        path = Path(path)
        with path.open("r", encoding="utf-8") as fp:
            cfg_with_env = os.path.expandvars(fp.read())
            data: dict[str, Any] = yaml.load(cfg_with_env, Loader=yaml.FullLoader)
            return cast_with_type(data)
