"""Filters for usage in pathfinding."""

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Union

EdgeData = tuple[str, str, dict]
EdgeList = Iterable[EdgeData]

EdgeDataExtractor = Callable[[EdgeData, Any], Any]

@dataclass
class UseValIfNone:
    processor: Callable[[EdgeData], Any]

    def __call__(self, edge: EdgeData, val: Any):
        result = self.processor(edge)
        if result is None:
            return val
        return result
    
@dataclass
class UseDefaultIfNone:
    processor: Callable[[EdgeData], Any]
    default: Any

    def __call__(self, edge: EdgeData, _):
        result = self.processor(edge)
        if result is None:
            return self.default
        return result

@dataclass
class ProcessEdgeAttribute:
    attribute: str
    processor: Callable[[Any], Any] = None

    def __call__(self, edge: EdgeData):
        result = edge[2].get(self.attribute)
        if self.processor:
            return self.processor(result)
        return result

class EdgeFilter:

    def __init__(
        self,
        comparator: Callable[[Any, Any], bool],
        get_func: Union[EdgeDataExtractor, str],
        preprocessor: Callable[[Any], Any] = None
    ):
        self.comparator = comparator
        
        if isinstance(get_func, str):
            get_func = UseValIfNone(ProcessEdgeAttribute(get_func))

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

    def __call__(
        self,
        value: Any
    ):
        if not isinstance(value, self.types):
            raise TypeError(f"Expected type: {self.types}")
        return value

@dataclass
class TypeDifferentiatedProcessor:
    preprocessors: dict[Union[type, tuple[type]], Callable[[Any], Any]] = None

    def __call__(
        self,
        value: Any
    ):
        for expected_types, processor in self.preprocessors.items():
            if isinstance(value, expected_types):
                if processor:
                    return processor(value)
                return value
        raise TypeError(f"Expected types: {self.preprocessors.keys()}")
