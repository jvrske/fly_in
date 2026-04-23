from mapbuilder.hub import Hub
from mapbuilder.edge import Link


class Drone():
    def __init__(self, name: str, start: Hub, path: list[Hub]) -> None:
        self.name = name
        self.vertex = start
        self.path = path
        self.arrived = False
        self.in_transit = False
        self.transit_edge = None
        self.destination = None

    def has_path(self) -> bool:
        """Return True if the drone still has steps left"""
        return len(self.path) > 0

    def next_hub(self) -> Hub | None:
        """Return the immediate next hub in the path"""
        return self.path[-1] if self.path else None

    def walk(self) -> None:
        """Advance the drone by one simulation turn"""
        if self.in_transit:
            dest = self.destination
            edge = self.transit_edge

            dest.drones.append(self)
            self.vertex = dest
            edge.reset_n_drones()
            self.in_transit = False
            self.transit_edge = None
            self.destination = None

        if not self.has_path():
            return None

        used_edge = self.vertex.get_edge(self.path[-1])
        if self.path[-1].is_possible() and used_edge.is_available():
            self.vertex.drones.remove(self)
            used_edge.att_n_drones()
            self.path[-1].drones.append(self)
            self.vertex = self.path[-1]
            self.path.pop()
            return f"{self.name}-{self.vertex.name}"

        if not self.path[-1].is_possible():
            self.vertex.drones.remove(self)
            used_edge.att_n_drones()
            self.path.pop()
            self.in_transit = True
            self.destination = self.path[-1]
            self.transit_edge = used_edge
            return f"{self.name}-{self.vertex.name}>{self.path[-1].name}"
