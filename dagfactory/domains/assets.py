from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union
from airflow.sdk import Asset, AssetAll

import re

@dataclass
class AssetCustomConfig:
    file: str
    datasets: Union[str, List[str]]

    @property
    def get_conditions_expression(self) -> str:
        if isinstance(self.datasets, str):
            return self.datasets
        elif isinstance(self.datasets, list):
            return " & ".join(self.datasets)
        else:
            raise ValueError("datasets must be a string or a list of strings")

@dataclass
class AssetMetadata:
    uri: str
    name: Optional[str] = field(default=None)
    def __post_init__(self):
        if self.name is None:
            self.name = self.uri
    @property
    def variable_name(self) -> str:
        sanitized: str = re.sub(r"[^\w]+", "_", self.name)
        if sanitized and sanitized[0].isdigit():
            sanitized = "_" + sanitized
        return sanitized
    
    @property
    def asset(self) -> Asset:
        return Asset(name=self.name, uri=self.uri)

@dataclass
class AssetMapper:
    assets_conditions: str
    assets_map: Dict[str, Asset] = field(default_factory=dict)

    def add_mapping(self, asset_metadata: AssetMetadata):
        variable_name = asset_metadata.variable_name
        self.assets_conditions = self.assets_conditions.replace(asset_metadata.name, variable_name)
        self.assets_map[variable_name] = asset_metadata.asset

    @property
    def extract_dataset_names(self) -> List[str]:
        expr = self.assets_conditions
        for storage in self.extract_storage_names:
            expr = expr.replace(storage, "")
        dataset_pattern = r"\b[a-zA-Z_][a-zA-Z0-9_\-./\\]*\b"
        datasets = re.findall(dataset_pattern, expr)
        return datasets
    
    @property
    def extract_storage_names(self) -> List[str]:
        storage_pattern = r"[a-zA-Z][a-zA-Z0-9+.-]*://[a-zA-Z0-9\-_/\.]+"
        storages = re.findall(storage_pattern, self.assets_conditions)
        return storages

    

