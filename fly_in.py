from parser import Parser
from mapbuilder.map import Map
from mapbuilder.hub import Hub
from mapbuilder.edge import Link


if __name__ == "__main__":
    cfg = Parser.parser("maps/hard/02_capacity_hell.txt")
    map = Map(**cfg)
