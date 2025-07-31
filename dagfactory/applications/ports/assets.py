from abc import ABC, abstractmethod
from airflow.sdk import Asset, AssetAll
import re
from typing import Optional, List, Any, Dict, Union

class IAssetBuilder(ABC):
    @abstractmethod
    def build(self) -> AssetAll:
        raise NotImplementedError()
    
    def extract_dataset_names(self, expression: str) -> List[str]:
        expr = expression
        for storage in self.extract_storage_names(expression):
            expr = expr.replace(storage, "")
        dataset_pattern = r"[a-zA-Z_][a-zA-Z0-9_\-./\\]*"
        datasets = re.findall(dataset_pattern, expr)
        return datasets
    
    def extract_storage_names(self, expression: str) -> List[str]:
        storage_pattern = r"[a-zA-Z][a-zA-Z0-9+.-]*://[a-zA-Z0-9\-_/\.]+"
        storages = re.findall(storage_pattern, expression)
        return storages
