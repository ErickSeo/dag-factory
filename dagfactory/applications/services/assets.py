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
    AssetMapper,
)


@dataclass
class AssetsCustomConfigBuilder(IAssetBuilder):
    entity: AssetCustomConfig
    airflow_version: AirflowVersion = field(default_factory=AirflowVersion)
    asset_mapper: AssetMapper = field(init=False)

    @property
    def file(self) -> str:
        return self.entity.file

    def _evaluate_conditions(self) -> AssetAll:
        evaluator = SafeEvalVisitor(
            source=self.asset_mapper.assets_conditions,
            node_map=self.asset_mapper.assets_map
        )
        evaluated_map = evaluator.evaluate()
        return evaluated_map

    def __build_metadata_list(self, assets: List[str]) -> None:
        for uri in assets:
            asset_metadata = AssetMetadata(uri=uri)
            self.asset_mapper.add_mapping(asset_metadata)

    def _build_for_new_version(self, filters: List[str]) -> None:
        raw_map: Dict[str, str] = get_datasets_map_uri_yaml_file(self.file, filters)
        not_in_config_file = list(filter(lambda x: x not in raw_map, filters))
        self.__build_metadata_list(not_in_config_file)
        for name, uri in raw_map.items():
            asset_metadata = AssetMetadata(name=name, uri=uri)
            self.asset_mapper.add_mapping(asset_metadata)

    def _build_for_old_version(self, filters: List[str]) -> None:
        assets: List[str] = get_datasets_uri_yaml_file(self.file, filters)
        not_in_config_file = list(filter(lambda x: x not in assets, filters))
        self.asset_mapper.assets_conditions = self.entity.get_conditions_expression
        self.__build_metadata_list(assets+not_in_config_file)

    def build(self) -> AssetAll:
        self.asset_mapper = AssetMapper(self.entity.get_conditions_expression)
        filters: List[str] = []
        filters.extend(self.asset_mapper.extract_dataset_names)
        filters.extend(self.asset_mapper.extract_storage_names)
        if self.airflow_version.is_at_least("2.9.0"):
            self._build_for_new_version(filters)
        else:
            self._build_for_old_version(filters)
        assets: AssetAll = self._evaluate_conditions()
        return assets
