from functools import reduce
from typing import Any, Dict, List, Union
from airflow.sdk import Asset

def combine_assets(assets: List[Asset], op: str) -> Asset:
    ops = {
        "and": lambda a, b: a & b,
        "or":  lambda a, b: a | b,
    }
    if op not in ops:
        raise ValueError(f"Unknown operator: {op!r}")
    return reduce(ops[op], assets)

def contains_asset(data: Dict[str, Any]) -> bool:
        if not isinstance(data, dict):
            return False
            
        for key, value in data.items():
            if isinstance(value, Asset):
                return True
            elif isinstance(value, list):
                if any(isinstance(item, Asset) for item in value):
                    return True
            elif isinstance(value, dict):
                if contains_asset(value):
                    return True
        return False

def parse_asset_schedule(value: Union[Dict, List, Asset]) -> Union[Asset, List[Asset]]:
    if isinstance(value, dict):
        if "or" in value:
            assets = [parse_asset_schedule(item) for item in value["or"]]
            return combine_assets(assets, "or")
        elif "and" in value:
            assets = [parse_asset_schedule(item) for item in value["and"]]
            return combine_assets(assets, "and")
    elif isinstance(value, list):
        return [asset for asset in value if isinstance(asset, Asset)]
    elif isinstance(value, Asset):
        return value
    else:
        raise TypeError(f"Unexpected data type: {type(value)}")

