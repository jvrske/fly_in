from mapbuilder.hub import Hub
from mapbuilder.edge import Link


class Drone():
    def __init__(self, name: str, vertex: Hub, path: list[Hub]) -> None:
        self.name = name
        self.vertex = vertex
        self.path = path

    def walk(self) -> None:
        used_edge = self.vertex.get_edge(self.path[-1])

        if self.path[-1].is_possible() and used_edge.is_available():
            self.vertex.drones.remove(self)
            used_edge.att_n_drones()
            self.path[-1].drones.append(self)
            self.vertex = self.path[-1]
            self.path.pop()
