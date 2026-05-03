from mapbuilder.map import Map
from drone import Drone


class Simulator():
    def __init__(self, graph: Map, n_drones: int) -> None:
        self.graph = graph
        self.turn = 0
        self.drones = []

        for i in range(n_drones):
            name = f"D{i + 1}"
            drone = Drone(name, self.graph.start)
            self.drones.append(drone)
            self.graph.start.drones.append(drone)

    def reset_edges(self) -> None:
        transit_edges = {d.transit_edge for d in self.drones if d.in_transit}
        all_edges = set()
        for hub in self.graph.hubs:
            for edge in hub.edges:
                all_edges.add(edge)

        for edge in all_edges - transit_edges:
            edge.reset_n_drones()

    def all_arrived(self) -> bool:
        return all(d.arrived for d in self.drones)

    def run(self) -> None:
        """run the simulation until all drones arrive or deadlock"""
        while not self.all_arrived():
            self.turn += 1
            turn_moves = []

            for drone in self.drones:
                if not drone.arrived:
                    result = drone.walk()
                    if result is not None:
                        turn_moves.append(result)
            if not turn_moves and not self.all_arrived():
                print("Error: deadlock detected")
                break
            if turn_moves:
                print(" ".join(turn_moves))
            self.reset_edges()
