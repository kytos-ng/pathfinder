from networkx import Graph, shortest_path
from networkx.exception import NodeNotFound

class KytosGraph:

    graph = None

    def __init__(self):
        self.graph = Graph()

    def clear(self):
        """Remove all nodes and links registered."""
        self.graph.clear()

    def update_nodes(self, nodes=[]):
        """Update all nodes inside the graph."""
        if not nodes:
            return
        for node in nodes:
           self.graph.add_node(node.device_id, ports=node.ports)

    def update_links(self, links=[]):
        """Update all links inside the graph."""
        if not links:
            return
        for link in links:
            source = link.interface_one.device.device_id
            destination = link.interface_two.device.device_id
            self.graph.add_edge(source, destination, object=link)

    def shortest_path(self, source, destination):
        """Calculate the shortest path and return it."""
        path = None
        try:
            path = shortest_path(self.graph, source, destination)
        except NodeNotFound:
            path = f"The shortest path between {source} and {destination}"
            path += " can't be found."
        return path