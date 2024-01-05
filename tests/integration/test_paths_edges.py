"""Module to test the KytosGraph in graph.py."""
import pytest
from itertools import combinations

# pylint: disable=import-error
from tests.integration.edges_settings import EdgesSettings


class TestPathsEdges(EdgesSettings):
    """TestPathsEdges."""

    @pytest.mark.parametrize("source,destination",
                             combinations(["User1", "User2", "User3", "User4"], 2))
    def test_k_shortest_paths_among_users(self, source, destination):
        """Tests paths between all users using unconstrained path algorithm."""
        self.initializer()
        paths = self.graph.k_shortest_paths(source, destination)
        assert paths
        for path in paths:
            assert path[0] == source
            assert path[-1] == destination

    @pytest.mark.parametrize("source,destination",
                             combinations(["User1", "User2", "User3", "User4"], 2))
    def test_constrained_k_shortest_paths_among_users(self, source, destination):
        """Tests paths between all users using constrained path algorithm,
        with no constraints set.
        """
        self.initializer()
        paths = self.graph.constrained_k_shortest_paths(
            source, destination
        )
        assert paths
        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination

    def test_cspf_delay_spf_attribute_between_u1_u4(self):
        """Test CSPF delay spf attribute between user1 and user4."""
        self.initializer()
        source = "User1"
        destination = "User4"
        spf_attribute = "delay"
        paths = self.graph.constrained_k_shortest_paths(
            source, destination, weight=spf_attribute
        )
        assert paths
        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
        paths = self.graph.path_cost_builder(paths, weight=spf_attribute)
        assert paths[0]["cost"] == 105 + 1 + 1

    def test_cspf_reliability_between_u1_u2(self):
        """Test CSPF reliability constraint between user1 and user2."""
        self.initializer()
        source = "User1"
        destination = "User2"
        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"reliability": 10}
        )
        assert not paths

        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"reliability": 3}
        )
        assert paths

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
            assert path["metrics"] == {"reliability": 3}
        paths = self.graph.path_cost_builder(paths)
        assert paths[0]["cost"] == 12

    def test_cspf_bandwidth_between_u1_u4(self):
        """Test CSPF bandwidth constraint between user1 and user4."""
        self.initializer()
        source = "User1"
        destination = "User4"
        spf_attribute = "delay"
        paths = self.graph.constrained_k_shortest_paths(
            source,
            destination,
            weight=spf_attribute,
            mandatory_metrics={"bandwidth": 200},
        )
        assert not paths

        paths = self.graph.constrained_k_shortest_paths(
            source,
            destination,
            weight=spf_attribute,
            mandatory_metrics={"bandwidth": 100},
        )
        assert paths

        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
            assert path["metrics"] == {"bandwidth": 100}
        paths = self.graph.path_cost_builder(paths, weight=spf_attribute)
        assert paths[0]["cost"] == 122

    def test_cspf_delay_between_u2_u3(self):
        """Test CSPF delay constraint between user2 and user3."""
        self.initializer()
        source = "User2"
        destination = "User3"

        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"delay": 1}
        )
        assert not paths

        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"delay": 50}
        )
        assert paths
        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
        paths = self.graph.path_cost_builder(paths)
        assert paths[0]["cost"] >= 3

    def test_cspf_ownership_between_s4_s6(self):
        """Test CSPF ownership constraint between switch4 and switch6."""
        self.initializer()
        source = "S6:2"
        destination = "S4:2"

        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"ownership": "B"}
        )
        assert not paths

        paths = self.graph.constrained_k_shortest_paths(
            source, destination, mandatory_metrics={"ownership": "A"}
        )
        assert paths
        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
        paths = self.graph.path_cost_builder(paths)
        assert paths[0]["cost"] >= 3

    def test_cspf_flexible_between_s4_s6(self):
        """Test CSPF flexible constraint between switch4 and switch6."""
        self.initializer()
        source = "S6:2"
        destination = "S4:2"

        paths = self.graph.constrained_k_shortest_paths(
            source,
            destination,
            mandatory_metrics={"reliability": 2},
            flexible_metrics={"bandwidth": 60},
            minimium_hits=1,
        )
        assert paths
        for path in paths:
            assert path["hops"][0] == source
            assert path["hops"][-1] == destination
        paths = self.graph.path_cost_builder(paths)
        assert paths[0]["cost"] >= 3

    def test_cspf_paths_mandatory_with_flexible(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with all but ownership flexible
        """
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        for source, destination in combos:
            paths = self.graph.constrained_k_shortest_paths(
                source,
                destination,
                mandatory_metrics={"ownership": "B"},
                flexible_metrics={
                    "delay": 50,
                    "bandwidth": 100,
                    "reliability": 3,
                },
            )
            for path in paths:
                hops_set = set(path["hops"])

                # delay = 50 checks
                if "delay" in path["metrics"]:
                    nodes = set([
                        "S1:1", "S2:1", "S3:1", "S5:1", "S4:2", "User1:2",
                        "S5:5", "S8:2", "S5:6", "User1:3", "S6:3", "S9:1",
                        "S6:4", "S9:2", "S6:5", "S10:1", "S8:5", "S9:4",
                        "User1:4", "User4:3"
                    ])
                    assert not nodes & hops_set

                # bandwidth = 100 checks
                if "bandwidth" in path["metrics"]:
                    nodes = set(["S3:1", "S5:1", "User1:4", "User4:3"])
                    assert not nodes & hops_set

                # reliability = 3 checks
                if "reliability" in path["metrics"]:
                    nodes = set(["S4:1", "S5:2", "S5:3", "S6:1"])
                    assert not nodes & hops_set

                # ownership = "B" checks
                assert "ownership" in path["metrics"]
                nodes = set([
                    "S4:1", "S5:2", "User1:2", "S5:4",
                    "S6:2", "S6:5", "S10:1", "S8:6", "S10:2",
                    "S10:3", "User2:1"
                ])
                assert not nodes & hops_set

    def test_ownership_type_error(self):
        """Tests that TypeError."""
        self.initializer()

        with pytest.raises(TypeError):
            self.graph.constrained_k_shortest_paths(
                "User1", "User2", mandatory_metrics={"ownership": 1}
            )
