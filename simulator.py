from mapbuilder.map import Map
from drone import Drone

COLOR_MAP = {
    "green": "\033[32m",
    "red": "\033[31m",
    "blue": "\033[34m",
    "orange": "\033[38;5;208m",
    "purple": "\033[35m",
    "brown": "\033[38;5;130m",
    "gold": "\033[93m",
    "violet": "\033[35m",
    "crimson": "\033[91m",
    "rainbow": "\033[95m",
    "darkred": "\033[31m",
    "cyan": "\033[36m",
    "lime": "\033[92m",
    "magenta": "\033[35m",
    "yellow": "\033[93m"
}

RESET = "\033[0m"


class Simulator():
    """manages turn-based simulation of drones navigating from start to end"""
    def __init__(self, graph: Map, n_drones: int,
                 visual: bool = False) -> None:
        self.graph = graph
        self.turn = 0
        self.drones: list[Drone] = []
        self.visual = visual
        self.hub_index = {h.name: h for h in graph.hubs}

        for i in range(n_drones):
            name = f"D{i + 1}"
            drone = Drone(name, self.graph.start)
            self.drones.append(drone)
            self.graph.start.drones.append(drone)

    def reset_edges(self) -> None:
        """reset edge drone counts, preserving edges occupied by in-transit
        drones"""
        transit_edges = {d.transit_edge for d in self.drones if d.in_transit}
        all_edges = set()
        for hub in self.graph.hubs:
            for edge in hub.edges:
                all_edges.add(edge)

        for edge in all_edges - transit_edges:
            edge.reset_n_drones()

    def all_arrived(self) -> bool:
        """return True if all drones have reached the end zone"""
        return all(d.arrived for d in self.drones)

    def paint(self, name: str) -> str:
        """return the hub name wrapped in its ANSI color code, or plain if no
        color"""
        hub = self.hub_index.get(name)

        if hub is None:
            return name

        color = COLOR_MAP.get(hub.color or "", "")
        return f"{color}{name}{RESET}"

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
                if self.visual:
                    painted = []
                    for move in turn_moves:
                        drone_name, rest = move.split("-", 1)
                        drone_name = f"\033[1m{drone_name}\033[0m"
                        if ">" in rest:
                            a, b = rest.split(">")
                            painted.append(
                                f"{drone_name}-{self.paint(a)}>{self.paint(b)}"
                                )
                        else:
                            painted.append(f"{drone_name}-{self.paint(rest)}")
                    print(" ".join(painted))
                else:
                    print(" ".join(turn_moves))
                self.reset_edges()
        print(self.turn)
