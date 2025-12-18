"""pathfinder Exceptions."""


class LinkNotFound(Exception):
    """Error when a link is not found in the graph."""
    def __init__(self, msg, link=None):
        self.link = link
        super().__init__(msg)
