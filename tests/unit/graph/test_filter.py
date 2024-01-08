"""Test filter methods"""
# pylint: disable=protected-access
import pytest
from unittest.mock import MagicMock

from napps.kytos.pathfinder.graph.filters import (TypeCheckPreprocessor,
                                                  TypeDifferentiatedProcessor)
from napps.kytos.pathfinder.graph import KytosGraph


class TestLazyFilter:
    """Tests for the Main class."""

    def setup_method(self):
        """Execute steps before each test."""
        self.graph = KytosGraph()

    def test_type_error(self):
        """Test filtering with invalid minimum type."""
        wrong_type = "wrong_type"
        right_type = 3
        preprocessor = TypeCheckPreprocessor(int)
        with pytest.raises(TypeError):
            preprocessor(wrong_type)
        preprocessor(right_type)

    def test_type_error2(self):
        """Test filtering with invalid minimum type."""
        wrong_type = "wrong_type"
        right_type = 3
        fake_inner = MagicMock()
        preprocessor = TypeDifferentiatedProcessor({
                int: fake_inner
        })
        with pytest.raises(TypeError):
            preprocessor(wrong_type)
        fake_inner.assert_not_called()
        preprocessor(right_type)
        fake_inner.assert_called_once()

    def test_filter_functions_in(self):
        """Test _filter_function that are expected to use the filter_in""" ""

        attr = "ownership"
        nx_edge_values = [
            (None, None, {attr: {"blue": {}, "red": {}}}),
            (None, None, {attr: {"green": {}}}),
        ]

        target = "blue"
        ownership_filter = self.graph._filter_functions[attr]
        filtered = list(ownership_filter(target, nx_edge_values))
        assert filtered

        for item in filtered:
            assert target in item[2][attr]

    def test_filter_functions_ge(self):
        """Test _filter_function that are expected to use the filter_ge."""

        for attr in ("bandwidth", "reliability"):
            nx_edge_values = [
                (None, None, {attr: 20}),
                (None, None, {attr: 10}),
            ]

            target = 15
            func = self.graph._filter_functions[attr]
            filtered = list(func(target, nx_edge_values))
            assert filtered

            for item in filtered:
                assert item[2][attr] >= target

            target = 21
            filter_func = self.graph._filter_functions[attr]
            filtered = list(filter_func(target, nx_edge_values))
            assert not filtered

    def test_filter_functions_le(self):
        """Test _filter_function that are expected to use the filter_le."""

        for attr in ("priority", "delay", "utilization"):
            nx_edge_values = [
                (None, None, {attr: 20}),
                (None, None, {attr: 10}),
            ]

            target = 15
            func = self.graph._filter_functions[attr]
            filtered = list(func(target, nx_edge_values))
            assert filtered

            for item in filtered:
                assert item[2][attr] <= target

            target = 9
            filter_func = self.graph._filter_functions[attr]
            filtered = list(filter_func(target, nx_edge_values))
            assert not filtered
