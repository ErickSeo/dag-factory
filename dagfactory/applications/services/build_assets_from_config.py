from dataclasses import dataclass, field
from airflow.sdk import Asset, AssetAll, AssetAny
from typing import List, Any, Dict, Union, Tuple
from dagfactory.domains.ports import (
    IConfigLoader, 
    IPyparsingExpressionParser,
    AssetExpr
)

from dagfactory.utils import (
    cast_with_type,
)

from dagfactory.applications.ports import IAssetBuilder
from dagfactory.infrastructures import (
    PyparsingExpressionParser,
    YamlConfigLoader,
    parse_asset_schedule,
)
from dagfactory.domains.entities import (
    AssetCustomConfig,
)

LeafLocation = Tuple[List[AssetExpr], int]

@dataclass
class BuildAssetsFromConfig(IAssetBuilder):
    entity: AssetCustomConfig
    config_loader: IConfigLoader = field(default_factory=YamlConfigLoader, repr=False)
    parser: IPyparsingExpressionParser = field(default_factory=PyparsingExpressionParser, repr=False)

    @property
    def file(self) -> str:
        return self.entity.file

    def _build_for_new_version(self, 
                               custom_configs: List[str],
                               asset_expression: AssetExpr
    ) -> None:
        config_map = {cfg["name"]: cfg for cfg in custom_configs}
        for leaf, setter in self.parser.traverse_with_setter(asset_expression):
            if leaf in config_map:
                cfg = config_map[leaf]
                cfg["__type__"] = self.entity.asset_type
                setter(cast_with_type(cfg))
            else:
                setter(Asset(leaf))

    def build(self)-> Union[AssetAll, AssetAny]:
        custom_configs: Dict[str, Any] = self.config_loader.load(self.file)
        asset_expression: AssetExpr = self.parser.parse(self.entity.get_conditions_expression)
        self._build_for_new_version(
            custom_configs=custom_configs.get(self.entity.key),
            asset_expression=asset_expression
        )
        assert_parsed: Union[AssetAll, AssetAny] = parse_asset_schedule(asset_expression)
        return assert_parsed
