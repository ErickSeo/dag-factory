from dataclasses import dataclass, field
from airflow.sdk import Asset, AssetAll

from typing import Optional, List, Any, Dict, Union
from dagfactory.utils import (
    get_datasets_map_uri_yaml_file,
    get_datasets_uri_yaml_file,
)

from dagfactory.applications.ports import IAssetBuilder
from dagfactory.infrastructures import SafeEvalVisitor
from dagfactory.domains import (
    AirflowVersion,
    AssetCustomConfig,
    AssetMetadata,
)


@dataclass
class AssetsCustomConfigBuilder(IAssetBuilder):
    entity: AssetCustomConfig
    airflow_version: AirflowVersion = field(default_factory=AirflowVersion)
    _assets_conditions: str = field(default_factory=str, init=False)
    _assets_map: Dict[str, Asset] = field(default_factory=dict, init=False)

    @property
    def file(self) -> str:
        return self.entity.file

    @property
    def assets_conditions(self) -> str:
        return " & ".join(self.entity.datasets)

    def _sanitize_conditions(self) -> List[str]:
        names: Optional[List[str]] = []
        names.extend(self.extract_dataset_names(self.assets_conditions))
        names.extend(self.extract_storage_names(self.assets_conditions))
        return names
    
    def __build_map(self, asset_metadata: AssetMetadata):
        variable_name = asset_metadata.variable_name
        self._assets_conditions = self._assets_conditions.replace(asset_metadata.uri, variable_name)
        self._assets_map[variable_name] = asset_metadata.asset

    def _build_map(self, filters: List[str]):
        raw_map: Dict[str, str] = get_datasets_map_uri_yaml_file(self.file, filters)
        self._assets_conditions = self.assets_conditions
        for name, uri in raw_map.items():
            asset_metadata = AssetMetadata(name=name, uri=uri)
            self.__build_map(asset_metadata)

    def _fallback(self, filters: List[str]):
        uris: List[str] = get_datasets_uri_yaml_file(self.file, filters)
        self._assets_conditions = " & ".join(uris)
        for uri in uris:
            asset_metadata = AssetMetadata(uri=uri)
            self.__build_map(asset_metadata)

    def _evaluate_conditions(self) -> AssetAll:        
        evaluator = SafeEvalVisitor(
            source=self._assets_conditions,
            node_map=self._assets_map
        )
        evaluated_map = evaluator.evaluate()
        return AssetAll(evaluated_map)

    def build(self) -> AssetAll:
        self._assets_map.clear()
        filters: List[str] = self._sanitize_conditions()
        if self.airflow_version.is_at_least("2.9.0"):
            self._build_map(filters)
        else:
            self._fallback(filters)
        assets:AssetAll = self._evaluate_conditions()
        return assets
