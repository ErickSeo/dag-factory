from dataclasses import dataclass, field
from typing import List, Optional
from airflow.sdk import Asset, AssetAll

import re

@dataclass
class AssetCustomConfig:
    file: str
    datasets: List[str]

    def get_conditions_expression(self) -> str:
        return " & ".join(self.datasets)
    
@dataclass
class AssetMetadata:
    uri: str
    name: Optional[str] = field(default=None)
    def __post_init__(self):
        if self.name is None:
            self.name = self.uri
    @property
    def variable_name(self):
        return re.sub(r"\W|^(?=\d)", "_", self.name)
    
    @property
    def asset(self) -> Asset:
        return Asset(name=self.name, uri=self.uri)
    