from parser import Parser
from simulator import Simulator
from mapbuilder.map import Map


if __name__ == "__main__":
    cfg = Parser.parser("maps/easy/01_linear_path.txt")
    graph = Map(**cfg)
    sim = Simulator(graph, graph.nb_drones)

    path = [graph.get_hub("goal"),
            graph.get_hub("waypoint2"),
            graph.get_hub("waypoint1")]

    for drone in sim.drones:
        drone.path = path.copy()

    sim.run()
