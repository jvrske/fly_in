import sys
from parser import Parser
from simulator import Simulator
from mapbuilder.map import Map
from algorithm.dijkstra import Dijkstra


if __name__ == "__main__":
    cfg = Parser.parser(sys.argv[1])
    graph = Map(**cfg)
    visual = "--visual" in sys.argv

    dijkstra = Dijkstra()
    path = dijkstra.solve(graph)

    sim = Simulator(graph, graph.nb_drones, visual=visual)
    for drone in sim.drones:
        drone.path = path.copy()

    sim.run()
