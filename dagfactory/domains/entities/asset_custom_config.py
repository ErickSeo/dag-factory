from dataclasses import dataclass, field
from typing import List, Union

@dataclass
class AssetCustomConfig:
    file: str
    datasets: Union[str, List[str]]
    key: str = field(default="datasets")
    asset_type: str = field(default="airflow.sdk.Asset")

    @property
    def get_conditions_expression(self) -> str:
        if isinstance(self.datasets, str):
            return self.datasets
        elif isinstance(self.datasets, list):
            return " & ".join(self.datasets)
        else:
            raise ValueError("datasets must be a string or a list of strings")