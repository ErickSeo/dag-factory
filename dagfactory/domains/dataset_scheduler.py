from dataclasses import dataclass
from typing import Optional, List, Any, Dict, Union
from airflow.sdk import Asset
from dagfactory import parsers, utils
from dagfactory.domains.airflow_version import AirflowVersion
import re
import ast
from abc import ABC, abstractmethod


@dataclass
class DatasetsWithFileBuilder(IAssetBuilder):
    file: str
    datasets_conditions: str
    assets: Dict[str, Asset]

    def parse(self) -> Dict[str, Asset]:
        assets: Dict[str, Asset] = dict()
        datasets_filter = list(self.assets.keys())
        if AirflowVersion().is_at_least("2.9.0"):            
            map_datasets = utils.get_datasets_map_uri_yaml_file(self.file, datasets_filter)
            dataset_map = {alias_dataset: self.to_asset(uri) for alias_dataset, uri in map_datasets.items()}
            eval_parser = DatasetsEvalCondition(self.datasets_conditions, dataset_map)
            assets = eval_parser.parse()
        else:
            datasets_uri = utils.get_datasets_uri_yaml_file(self.file, datasets_filter)
            for uri in datasets_uri:
                assets[uri] = self.to_asset(uri)
        return assets

@dataclass
class DataSetTransformer(IAssetBuilder):
    datasets_conditions: str

    def parse(self) -> Dict[str, Asset]:
        assets: Dict[str, Asset] = dict()
        datasets_filter: List[str] = []
        datasets_filter.extend(self.extract_dataset_names(self.datasets_conditions))
        datasets_filter.extend(self.extract_storage_names(self.datasets_conditions))

        for uri in datasets_filter:
            valid_variable_name = utils.make_valid_variable_name(uri)
            self.datasets_conditions = self.datasets_conditions.replace(uri, valid_variable_name)
            assets[uri] = self.to_asset(uri)
        return assets

@dataclass
class DataSetFallback(IAssetBuilder):
    datasets_conditions: List[str]

    def parse(self) -> Dict[str, Asset]:
        assets: Dict[str, Asset] = dict()
        datasets_filter: List[str] = []
        datasets_filter.extend(self.extract_dataset_names(self.datasets_conditions))
        datasets_filter.extend(self.extract_storage_names(self.datasets_conditions))

        for uri in datasets_filter:
            valid_variable_name = utils.make_valid_variable_name(uri)
            self.datasets_conditions = self.datasets_conditions.replace(uri, valid_variable_name)
            assets[uri] = self.to_asset(uri)
        return assets

# --------------------------------------------

class AssetBuilderFactory:
    datasets: Union[List[str], str]

    @staticmethod
    def create(self, schedule: Union[Dict, str]) -> IAssetBuilder:
        has_file_attr = utils.check_dict_key(schedule, "file")

        #has_datasets_attr = utils.check_dict_key(schedule, "datasets") fazer verificacao la
        datasets_conditions: str = " & ".join(self.datasets)
        DataSetTransformer(datasets_conditions)
        if has_file_attr:
            file = schedule.get("file")
            builder = DatasetsWithFileBuilder(file, datasets_conditions)
        elif AirflowVersion().is_at_least("2.9.0"):
            builder = DataSetTransformer(datasets_conditions)
            

# --------------------------------------------

# EXEMPLO DE USO:

# schedule = {"file": "some_file.yml", "datasets": ["dataset_custom_1", "dataset_custom_2"]}
# builder = AssetBuilderFactory.create(schedule)
# assets = builder.parse()

# schedule = "dataset_custom_1 & dataset_custom_2"
# builder = AssetBuilderFactory.create(schedule)
# assets = builder.parse()
