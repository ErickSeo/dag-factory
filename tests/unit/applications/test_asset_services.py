from typing import Dict, Any, List, Tuple
from automapper import mapper

from airflow.sdk import Asset, AssetAll, AssetAny
from packaging.version import Version, parse as parse_version


from dagfactory.applications.ports import IAssetBuilder
from dagfactory.domains import (
    AssetCustomConfig,
    AirflowVersion
)
from dagfactory.applications.services import (
    AssetsCustomConfigBuilder,
)


class TestAssetCustomConfig:
    filename = "custom_config.yml"
    airflow_2_9 = AirflowVersion(parse_version("2.9.0"))
    airflow_2_4 = AirflowVersion(parse_version("2.4.0"))

    def test_custom_config_array_assets(self, read_dataset_yaml):
        key = "example_array_alias"
        value: Dict[str, Any] = read_dataset_yaml(self.filename)
        
        entity_parsed = mapper.to(AssetCustomConfig).map(value.get(key)["schedule"])
        asset_service: IAssetBuilder = AssetsCustomConfigBuilder(entity=entity_parsed)
        result: AssetAll = asset_service.build()
        assert isinstance(result, AssetAll)
        for key, asset in list(result.iter_assets()):
            assert key.name in entity_parsed.datasets
            assert isinstance(asset, Asset)
    
    def test_custom_config_array_assets_2_4(self, read_dataset_yaml):
        key = "example_array_alias"
        value: Dict[str, Any] = read_dataset_yaml(self.filename)
        
        entity_parsed = mapper.to(AssetCustomConfig).map(value.get(key)["schedule"])
        asset_service: IAssetBuilder = AssetsCustomConfigBuilder(
                                                entity=entity_parsed,
                                                airflow_version=self.airflow_2_4
                                        )
        result: AssetAll = asset_service.build()
        assert isinstance(result, AssetAll)
    




        