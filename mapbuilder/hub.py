class Hub():
    def __init__(self, name: str, x: int, y: int,
                 metadata: dict | None = None):
        self.name = name
        self.xy = (x, y)
        self.color = None
        self.zone = 'normal'
        self.max_drones = 1
        self.drones = []
        self.links = []
        if metadata:
            self.metadata = metadata

    def __repr__(self):
        return self.name

    