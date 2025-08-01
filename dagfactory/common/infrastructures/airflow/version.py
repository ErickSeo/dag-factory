from airflow.version import version as AIRFLOW_VERSION
from dataclasses import dataclass, field
from packaging.version import Version, parse as parse_version
from typing import Union
import operator

@dataclass(frozen=True)
class AirflowVersion:
    airflow_version: Version = field(
        default_factory=lambda: parse_version(AIRFLOW_VERSION)
    )

    @staticmethod
    def _parse(ver: Union[str, Version]) -> Version:
        return ver if isinstance(ver, Version) else parse_version(ver)

    def compare(self, other: Union[str, Version], op: str = "ge") -> bool:
        """Compare with other version using operator.
        Supported ops: 'ge', 'gt', 'le', 'lt', 'eq', 'ne'
        """
        ops = {
            "ge": operator.ge,    # >=
            "gt": operator.gt,    # >
            "le": operator.le,    # <=
            "lt": operator.lt,    # <
            "eq": operator.eq,    # ==
            "ne": operator.ne,    # !=
        }
        if op not in ops:
            raise ValueError(f"Invalid comparison operator: {op}")
        return ops[op](self.airflow_version, self._parse(other))

    def is_at_least(self, v: Union[str, Version]) -> bool:
        return self.compare(v, "ge")

    def is_less_than(self, v: Union[str, Version]) -> bool:
        return self.compare(v, "lt")

    def is_equal(self, v: Union[str, Version]) -> bool:
        return self.compare(v, "eq")