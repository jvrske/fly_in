from mapbuilder.hub import Hub
from mapbuilder.edge import Link


class Drone():
    def __init__(self, name: str, start: Hub,
                 path: list[Hub] | None = None) -> None:
        self.name = name
        self.vertex = start
        self.path: list[Hub] = path if path is not None else []
        self.arrived = False
        self.in_transit = False
        self.transit_edge: Link | None = None
        self.destination: Hub | None = None

    def has_path(self) -> bool:
        """return True if the drone still has steps left"""
        return len(self.path) > 0

    def next_hub(self) -> Hub | None:
        """return the immediate next hub in the path"""
        return self.path[-1] if self.path else None

    def walk(self) -> str | None:
        """advance the drone by one simulation turn"""
        # arrived at destination
        if self.in_transit:
            dest = self.destination
            edge = self.transit_edge
            assert dest is not None and edge is not None

            if not dest.is_possible():
                return None

            dest.drones.append(self)
            self.vertex = dest
            if self.vertex == self.path[0]:
                self.arrived = True
            edge.reset_n_drones()
            self.in_transit = False
            self.transit_edge = None
            self.destination = None
            return f"{self.name}-{self.vertex.name}"

        if not self.has_path():
            return None

        target = self.path[-1]
        used_edge = self.vertex.get_edge(target)

        if used_edge is None:
            return None

        # normal zones and priority
        if target.zone != "restricted" and target.is_possible() \
                and used_edge.is_available():
            self.vertex.drones.remove(self)
            used_edge.att_n_drones()
            target.drones.append(self)
            self.vertex = target
            if self.vertex == self.path[0]:
                self.arrived = True
            self.path.pop()
            return f"{self.name}-{self.vertex.name}"

        # restricted zones
        if target.zone == "restricted":
            if not used_edge.is_available():
                return None

            self.vertex.drones.remove(self)
            used_edge.att_n_drones()
            self.destination = target
            self.path.pop()
            self.in_transit = True
            self.transit_edge = used_edge
            return f"{self.name}-{self.vertex.name}>{target.name}"

        return None
