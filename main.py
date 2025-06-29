"""Main module of kytos/pathfinder Kytos Network Application."""

import pathlib
from threading import Lock
from typing import Generator

from kytos.core import KytosNApp, log, rest
from kytos.core.helpers import listen_to, load_spec, validate_openapi
from kytos.core.rest_api import (HTTPException, JSONResponse, Request,
                                 get_json_or_400)
from napps.kytos.pathfinder.graph import KytosGraph


class Main(KytosNApp):
    """
    Main class of kytos/pathfinder NApp.

    This class is the entry point for this napp.
    """

    spec = load_spec(pathlib.Path(__file__).parent / "openapi.yml")

    def setup(self):
        """Create a graph to handle the nodes and edges."""
        self.graph = KytosGraph()
        self._topology = None
        self._lock = Lock()

    def execute(self):
        """Do nothing."""

    def shutdown(self):
        """Shutdown the napp."""

    def _filter_paths_le_cost(self, paths, max_cost):
        """Filter by paths where the cost is le <= max_cost."""
        if not max_cost:
            return paths
        return [path for path in paths if path["cost"] <= max_cost]

    def _non_excluded_edges(self, links: list[str]) -> list[tuple[str, str]]:
        """Exlude undesired links. It'll return the remaning edges."""

        endpoints: list[tuple[str, str]] = []
        if not self._topology:
            return endpoints
        endpoint_ids = self._map_endpoints_from_link_ids(links)
        for edge in self.graph.graph.edges:
            if edge not in endpoint_ids:
                endpoints.append(edge)
        return endpoints

    def _map_endpoints_from_link_ids(self, link_ids: list[str]) -> dict:
        """Map endpoints from link ids."""
        endpoints = {}
        for link_id in link_ids:
            try:
                link = self._topology.links[link_id]
                endpoint_a, endpoint_b = link.endpoint_a, link.endpoint_b
                endpoints[(endpoint_a.id, endpoint_b.id)] = link
            except KeyError:
                pass
        return endpoints

    def _find_all_link_ids(
        self, paths: list[dict], link_ids: list[str]
    ) -> Generator[int, None, None]:
        """Find indexes of the paths that contain all link ids."""
        endpoints_links = self._map_endpoints_from_link_ids(link_ids)
        if not endpoints_links:
            return None
        endpoint_keys = set(endpoints_links.keys())
        for idx, path in enumerate(paths):
            head, tail, found_endpoints = path["hops"][:-1], path["hops"][1:], set()
            for endpoint_a, endpoint_b in zip(head, tail):
                if (endpoint_a, endpoint_b) in endpoints_links:
                    found_endpoints.add((endpoint_a, endpoint_b))
                if (endpoint_b, endpoint_a) in endpoints_links:
                    found_endpoints.add((endpoint_b, endpoint_a))
            if found_endpoints == endpoint_keys:
                yield idx
        return None

    @rest("v3/", methods=["POST"])
    @validate_openapi(spec)
    def shortest_path(self, request: Request) -> JSONResponse:
        """Calculate the best path between the source and destination."""
        data = get_json_or_400(request, self.controller.loop)
        if not isinstance(data, dict):
            raise HTTPException(400, detail=f"Invalid body value: {data}")

        undesired = data.get("undesired_links", [])
        spf_attr = data.get("spf_attribute", "hop")
        spf_max_paths = data.get("spf_max_paths", 2)
        spf_max_path_cost = data.get("spf_max_path_cost")
        mandatory_metrics = data.get("mandatory_metrics", {})
        flexible_metrics = data.get("flexible_metrics", {})
        minimum_hits = data.get("minimum_flexible_hits")
        log.debug(f"POST v2/ payload data: {data}")

        try:
            with self._lock:
                self._get_latest_topology()
                graph = self.graph.graph
                if undesired:
                    non_excluded_edges = self._non_excluded_edges(undesired)
                    graph = graph.edge_subgraph(non_excluded_edges)

                if any([mandatory_metrics, flexible_metrics]):
                    paths = self.graph.constrained_k_shortest_paths(
                        data["source"],
                        data["destination"],
                        weight=self.graph.spf_edge_data_cbs[spf_attr],
                        k=spf_max_paths,
                        graph=graph,
                        minimum_hits=minimum_hits,
                        mandatory_metrics=mandatory_metrics,
                        flexible_metrics=flexible_metrics,
                    )
                else:
                    paths = self.graph.k_shortest_paths(
                        data["source"],
                        data["destination"],
                        weight=self.graph.spf_edge_data_cbs[spf_attr],
                        k=spf_max_paths,
                        graph=graph,
                    )

                paths = self.graph.path_cost_builder(
                    paths,
                    weight=spf_attr,
                )
            log.debug(f"Found paths: {paths}")
        except TypeError as err:
            raise HTTPException(400, str(err))

        paths = self._filter_paths_le_cost(paths, max_cost=spf_max_path_cost)
        log.debug(f"Filtered paths: {paths}")
        return JSONResponse({"paths": paths})

    @listen_to(
        "kytos.topology.updated",
        "kytos/topology.topology_loaded",
        pool="dynamic_single"
    )
    def on_topology_updated(self, event):
        """Update the graph when the network topology is updated."""
        self.update_topology(event)

    def update_topology(self, event):
        """Update the graph when the network topology is updated."""
        if "topology" not in event.content:
            return
        topology = event.content["topology"]
        with self._lock:
            self._update_to_topology(topology)

    def _get_latest_topology(self):
        """Get the latest topology from the topology napp."""
        try:
            topology_napp = self.controller.napps[("kytos", "topology")]
        except KeyError:
            log.warning("Failed to get topology napp for forcing topology update.")
            return
        topology = topology_napp.get_latest_topology()
        self._update_to_topology(topology)

    def _update_to_topology(
        self,
        topology
    ):
        if self._topology is topology:
            return

        self._topology = topology
        self.graph.update_topology(topology)

        switches = list(topology.switches.keys())
        links = list(topology.links.keys())
        log.debug(f"Topology graph updated with switches: {switches}, links: {links}.")
