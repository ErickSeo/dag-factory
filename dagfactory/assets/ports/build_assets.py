from abc import ABC, abstractmethod
from typing import Union
from airflow.sdk import AssetAll, AssetAny

class IAssetBuilderPort(ABC):
    @abstractmethod
    def build(self) -> Union[AssetAll, AssetAny]:
        raise NotImplementedError()
    
