from abc import ABC, abstractmethod
from typing import Union
from airflow.sdk import AssetAll, AssetAny

class ITriggerBuilderPort(ABC):
    @abstractmethod
    def build(self) -> Union[AssetAll, AssetAny]:
        raise NotImplementedError()
    
