from mapbuilder.hub import Hub
from mapbuilder.edge import Link


class Drone():
    def __init__(self, name: str, start: Hub, path: list[Hub]) -> None:
        self.name = name
        self.vertex = start
        self.path = path
        self.arrived = False
        self.in_transit = False
        self.transit_edge = Link | None
        self.destination = Hub | None

    def has_path(self) -> bool:
        """Return True if the drone still has steps left"""
        return len(self.path) > 0

    def next_hub(self) -> Hub | None:
        """Return the immediate next hub in the path"""
        return self.path[-1] if self.path else None

    def walk(self) -> str | None:
        """Advance the drone by one simulation turn"""
        # arrived at destination
        if self.in_transit:
            dest = self.destination
            edge = self.transit_edge

            dest.drones.append(self)
            self.vertex = dest
            edge.reset_n_drones()
            self.in_transit = False
            self.transit_edge = None
            self.destination = None
            return f"{self.name}-{self.vertex.name}"

        if not self.has_path():
            return None

        target = self.path[-1]
        used_edge = self.vertex.get_edge(target)

        # normal zones and priority
        if target.zone != "restricted" and target.is_possible() \
                and used_edge.is_available():
            self.vertex.drones.remove(self)
            used_edge.att_n_drones()
            target.drones.append(self)
            self.vertex = target
            self.path.pop()
            return f"{self.name}-{self.vertex.name}"

        # restricted zones
        if target.zone == "restricted":
            if not target.is_possible():
                return None

            self.vertex.drones.remove(self)
            used_edge.att_n_drones()
            self.destination = target
            self.path.pop()
            self.in_transit = True
            self.transit_edge = used_edge
            return f"{self.name}-{self.vertex.name}>{target.name}"

        return None
