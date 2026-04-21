from parser import Parser
from mapbuilder.map import Map
from mapbuilder.hub import Hub
from mapbuilder.link import Link


if __name__ == "__main__":
    cfg = Parser.parser("maps/hard/02_capacity_hell.txt")
    print(cfg["start_hub"])
    """ map = Map(**cfg) """