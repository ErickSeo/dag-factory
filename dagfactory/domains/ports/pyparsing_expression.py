from typing import Protocol, Generator, Tuple, Dict, List, Union, Callable

AssetExpr = Union[str, Dict[str, List["AssetExpr"]]]
LeafSetter = Callable[[str], None]


class IPyparsingExpressionParser(Protocol):
    def parse(self, expression: str) -> AssetExpr: 
        ...
        
    def traverse_with_setter(
        self,
        tree: AssetExpr
    ) -> Generator[Tuple[str, LeafSetter], None, None]:
        ...
