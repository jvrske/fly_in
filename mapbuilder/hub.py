class Hub():
    def __init__(self, name: str, x: int, y: int,
                 metadata: dict | None = None) -> None:
        self.name = name
        self.xy = (x, y)
        self.zone = "normal"
        self.max_drones = 1
        self.color = None
        if metadata:
            self.set_metadata(metadata)
        self.cost()
        self.links = []

    def is_accessible(self) -> bool:
        return self.zone != "blocked"

    def set_metadata(self, metadata: dict) -> None:
        for key, value in metadata.items():
            if key == "color":
                self.color = value
            elif key == "zone":
                self.zone = value
            else:
                self.max_drones = value

    def cost(self) -> None:
        if self.zone == "blocked":
            self.cost = 3
        elif self.zone == "priority":
            self.cost = -1
        elif self.zone == "restricted":
            self.cost = 2
        else:
            self.cost = 1
