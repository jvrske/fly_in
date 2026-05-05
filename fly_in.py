from parser import Parser
from simulator import Simulator
from mapbuilder.map import Map
from algorithm.dijkstra import Dijkstra


if __name__ == "__main__":
    cfg = Parser.parser("maps/challenger/01_the_impossible_dream.txt")
    graph = Map(**cfg)

    dijkstra = Dijkstra()
    path = dijkstra.solve(graph)

    sim = Simulator(graph, graph.nb_drones)
    for drone in sim.drones:
        drone.path = path.copy()

    sim.run()
