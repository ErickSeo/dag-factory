from typing import Dict, Any, List, Tuple, Union
from automapper import mapper

from airflow.sdk import Asset, AssetAll, AssetAny
from packaging.version import Version, parse as parse_version


from dagfactory.applications.ports import IAssetBuilder
from dagfactory.domains.entities import AssetCustomConfig
from dagfactory.infrastructures import AirflowVersion
from dagfactory.applications.services import BuildAssetsFromConfig
from dagfactory.infrastructures import PyparsingExpressionParser

AssetExpr = Union[str, Dict[str, List["AssetExpr"]]]

class TestAssetService:
    def test_parse_asset_expr(self):
        asset_service = PyparsingExpressionParser()
        expr_str = "asset1 & asset2 | asset3"
        expected = {'or': [{'and': ['asset1', 'asset2']}, 'asset3']}
        result: AssetExpr = asset_service.parse(expr_str)
        assert expected == result


class TestAssetCustomConfig:
    filename = "custom_config.yml"
    airflow_2_9 = AirflowVersion(parse_version("2.9.0"))
    airflow_2_4 = AirflowVersion(parse_version("2.4.0"))

    def test_custom_config_array_assets(self, read_dataset_yaml):
        key = "example_array_alias"
        value: Dict[str, Any] = read_dataset_yaml(self.filename)
        
        entity_parsed = mapper.to(AssetCustomConfig).map(value.get(key)["schedule"])
        asset_service: IAssetBuilder = BuildAssetsFromConfig(entity=entity_parsed)
        result: AssetAll = asset_service.build()
        assert isinstance(result, AssetAll)
        for key, asset in list(result.iter_assets()):
            assert key.name in entity_parsed.datasets
            assert isinstance(asset, Asset)
    
    def test_custom_config_string_conditions(self, read_dataset_yaml):
        key = "example_string_condition"
        value: Dict[str, Any] = read_dataset_yaml(self.filename)
        
        entity_parsed = mapper.to(AssetCustomConfig).map(value.get(key)["schedule"])
        asset_service: IAssetBuilder = BuildAssetsFromConfig(entity=entity_parsed)
        result: AssetAny = asset_service.build()
        assert isinstance(result, AssetAny)




        