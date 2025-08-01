from abc import ABC, abstractmethod
from typing import Union, Dict, List, Any
from airflow.sdk import Asset, AssetAll, AssetAny
AssetExpr = Union[str, Dict[str, List["AssetExpr"]]]

class IAssetBuilder(ABC):
    @abstractmethod
    def build(self) -> Union[AssetAll, AssetAny]:
        raise NotImplementedError()
    
