from dataclasses import dataclass, field
from typing import List, Optional, Dict
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

@dataclass
class AssetMapper:
    assets_conditions: str
    assets_map: Dict[str, Asset] = field(default_factory=dict)

    def add_mapping(self, asset_metadata: AssetMetadata):
        variable_name = asset_metadata.variable_name
        self.assets_conditions = self.assets_conditions.replace(asset_metadata.uri, variable_name)
        self.assets_map[variable_name] = asset_metadata.asset

    @property
    def extract_dataset_names(self) -> List[str]:
        dataset_pattern = r"\b[a-zA-Z_][a-zA-Z0-9_\-./\\]*\b"
        datasets = re.findall(dataset_pattern, self.assets_conditions)
        return datasets

    @property
    def extract_storage_names(self) -> List[str]:
        storage_pattern = r"[a-zA-Z][a-zA-Z0-9+.-]*://[a-zA-Z0-9\-_/\.]+"
        storages = re.findall(storage_pattern, self.assets_conditions)
        return storages

    

