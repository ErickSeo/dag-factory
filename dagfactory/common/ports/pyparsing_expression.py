from typing import Protocol, Generator, Tuple, Dict, List, Callable, Any


LeafSetter = Callable[[str], None]


class IPyparsingExpressionParser(Protocol):
    def parse(self, expression: str) -> Dict[str, List[Any]]: 
        ...
        
    def traverse_with_setter(
        self,
        tree: Dict[str, List[Any]]
    ) -> Generator[Tuple[str, LeafSetter], None, None]:
        ...
