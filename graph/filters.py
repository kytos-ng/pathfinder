"""Filters for usage in pathfinding."""

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Union

EdgeData = tuple[str, str, dict]
EdgeList = Iterable[EdgeData]

EdgeDataExtractor = Callable[[EdgeData, Any], Any]

class EdgeFilter:

    def __init__(
        self,
        comparator: Callable[[Any, Any], bool],
        get_func: Union[EdgeDataExtractor, str],
        preprocessor: Callable[[Any], Any] = None
    ):
        self.comparator = comparator
        
        if isinstance(get_func, str):
            get_str = get_func
            get_func = lambda edge, val: edge[2].get(get_str, val)

        self.get_func = get_func

        self.preprocessor = preprocessor

    def __call__(
        self,
        value: Any,
        items: EdgeList
    ) -> EdgeList:
        """Apply the filter given the items and value."""

        # Preprocess the value
        if self.preprocessor:
            value = self.preprocessor(value)
        
        # Run filter
        return filter(
            lambda edge:
                self.comparator(
                    self.get_func(edge, value),
                    value
            ),
            items
        )

@dataclass
class TypeCheckPreprocessor:
    types: Union[type, tuple[type]]
    preprocessor: Callable[[Any], Any] = None

    def __call__(
        self,
        value: Any
    ):
        if not isinstance(value, self.types):
            raise TypeError(f"Expected type: {self.types}")
        if self.preprocessor:
            return self.preprocessor(value)
        return value
