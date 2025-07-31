from abc import ABC, abstractmethod
from airflow.sdk import Asset, AssetAll
import re
from typing import Optional, List, Any, Dict, Union

class IAssetBuilder(ABC):
    @abstractmethod
    def build(self) -> AssetAll:
        raise NotImplementedError()
    