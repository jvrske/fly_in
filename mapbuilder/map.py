from .hub import Hub
from .edge import Link


class Map():
    def __init__(self, nb_drones: int, connection: list[dict],
                 start_hub: dict, end_hub: dict, hub: list[dict]):
        self.map = self.mapbuilder(start_hub, end_hub, hub, connection)

    def mapbuilder(self, start_hub: dict, end_hub: dict, hub: list[dict],
                   connection: list[dict]):
        map = []

        map.append(Hub(**start_hub))
        map.append(Hub(**end_hub))

        for h in hub:
            map.append(Hub(**h))

        for c in connection:
            vertex1 = None
            vertex2 = None

            for vertex in map:
                if vertex.name == c["zone1"]:
                    vertex1 = vertex
                if vertex.name == c["zone2"]:
                    vertex2 = vertex
            if vertex1 and vertex2:
                edge = Link(vertex1, vertex2, c.get("metadata"))
                vertex1.links.append(edge)
                vertex2.links.append(edge)
