from .hub import Hub
from typing import Any


class Link():
    """represents a bidirectional connection between two hubs"""

    def __init__(self, zone1: Hub, zone2: Hub,
                 metadata: dict[str, Any] | None = None) -> None:
        """initialize a Link"""
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link_capacity = 1
        self.n_drones = 0
        if metadata:
            self.set_metadata(metadata)

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        """apply connection metadata"""
        for key, value in metadata.items():
            if key == "max_link_capacity":
                self.max_link_capacity = value

    def is_available(self) -> bool:
        """return True if connection has capacity for one more drone"""
        return self.n_drones < self.max_link_capacity

    def att_n_drones(self) -> None:
        """increment the count of drones currently traversing this link"""
        self.n_drones += 1

    def reset_n_drones(self) -> None:
        """reset traversal count at end of turn"""
        self.n_drones = 0

    def get_current_hub(self, current: Hub) -> Hub | None:
        """return the hub matching current, or None"""
        if self.zone1 == current:
            return self.zone1
        if self.zone2 == current:
            return self.zone2
        return None

    def get_next_hub(self, current: Hub) -> Hub | None:
        """return the hub on the other side of this link"""
        if self.zone1 == current:
            return self.zone2
        if self.zone2 == current:
            return self.zone1
        return None
