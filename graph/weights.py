"""Weight functions for use in pathfinding."""
# pylint: disable=unused-argument

def nx_edge_data_weight(edge_u, edge_v, edge_data: dict):
    """Return custom edge data value to be used as a callback by nx."""
    return edge_data.get("hop", 1)


def nx_edge_data_delay(edge_u, edge_v, edge_data: dict):
    """Return custom edge data value to be used as a callback by nx."""
    return edge_data.get("delay", 1)


def nx_edge_data_priority(edge_u, edge_v, edge_data: dict):
    """Return custom edge data value to be used as a callback by nx."""
    return edge_data.get("priority", 1)
