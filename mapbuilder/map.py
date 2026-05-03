from .hub import Hub
from .edge import Link


class Map():
    """builds and holds the drone network graph"""

    def __init__(self, nb_drones: int, connection: list[dict],
                 start_hub: dict, end_hub: dict,
                 hub: list[dict]) -> None:
        """initialize the map from parsed data"""
        self.nb_drones = nb_drones
        self.start: Hub
        self.end: Hub
        self.hubs: list[Hub]
        self.build(start_hub, end_hub, hub, connection)

    def build(self, start_hub: dict, end_hub: dict, hub: list[dict],
              connection: list[dict]) -> None:
        """instantiate Hub and Link objects and wire them together"""
        self.start = Hub(**start_hub)
        self.end = Hub(**end_hub)
        self.hubs = [self.start, self.end] + [Hub(**h) for h in hub]
        hub_index: dict[str, Hub] = {h.name: h for h in self.hubs}

        for c in connection:
            v1 = hub_index.get(c["zone1"])
            v2 = hub_index.get(c["zone2"])
            if v1 and v2:
                edge = Link(v1, v2, c.get("metadata"))
                v1.edges.append(edge)
                v2.edges.append(edge)

    def get_hub(self, name: str) -> Hub | None:
        """find a hub by name"""
        for h in self.hubs:
            if h.name == name:
                return h
        return None
