from typing import Protocol, Mapping, Any

class IConfigLoader(Protocol):
    def load(self, path: str) -> Mapping[str, Any]: 
        ...