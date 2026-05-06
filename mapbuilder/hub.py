from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .edge import Link
    from drone import Drone


class Hub():
    """represents a zone/node in the drone network graph"""

    def __init__(self, name: str, x: int, y: int,
                 metadata: dict | None = None) -> None:
        """initialize a Hub"""
        self.name = name
        self.xy = (x, y)
        self.zone = "normal"
        self.max_drones = 1
        self.color = None
        if metadata:
            self.set_metadata(metadata)
        self.movement_cost = self._calc_cost()
        self.edges: list[Link] = []
        self.drones: list[Drone] = []

    def _calc_cost(self) -> int:
        """return movement cost based on zone type"""
        if self.zone == "blocked":
            return 3
        elif self.zone == "restricted":
            return 2
        else:
            return 1

    def set_metadata(self, metadata: dict) -> None:
        """apply metadata dict to hub attributes"""
        for key, value in metadata.items():
            if key == "color":
                self.color = value
            elif key == "zone":
                self.zone = value
            elif key == "max_drones":
                self.max_drones = value

    def is_accessible(self) -> bool:
        """return True if drones can enter this zone"""
        return self.zone != "blocked"

    def is_possible(self) -> bool:
        """return True if zone has capacity for one more drone"""
        return len(self.drones) < self.max_drones

    def get_edge(self, next_hub: 'Hub') -> Link | None:
        """return the Link connecting this hub to next_hub"""
        for edge in self.edges:
            if edge.get_next_hub(self) == next_hub:
                return edge
        return None
