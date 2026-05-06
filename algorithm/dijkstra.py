from mapbuilder.map import Map
from mapbuilder.hub import Hub
import heapq


class Dijkstra():
    """find shortest path from start to end using Dijkstra's algorithm"""
    def solve(self, graph: Map) -> list[Hub]:
        dist: dict[Hub, int] = {hub: int(999) for hub in graph.hubs}
        dist[graph.start] = 0
        prev: dict[Hub, Hub | None] = {hub: None for hub in graph.hubs}
        queue: list[tuple[float, int, Hub]] = [(0, 0, graph.start)]
        counter = 1

        while queue:
            actual_cost, _, actual_hub = heapq.heappop(queue)

            if actual_hub == graph.end:
                break

            if actual_cost > dist[actual_hub]:
                continue

            for edge in actual_hub.edges:
                neighbor = edge.get_next_hub(actual_hub)

                if neighbor is None:
                    continue
                if neighbor.zone == "blocked":
                    continue

                new_cost = dist[actual_hub] + neighbor.movement_cost

                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    prev[neighbor] = actual_hub
                    heapq.heappush(queue, (new_cost, counter, neighbor))
                    counter += 1
        return self.build_path(prev, graph)

    def build_path(self, prev: dict[Hub, Hub | None],
                   graph: Map) -> list[Hub]:
        """reconstruct path from prev dict. returns [end, ..., first_step]"""
        path: list[Hub] = []
        current: Hub | None = graph.end

        while current is not None:
            path.append(current)
            current = prev[current]
        path.pop()
        return path
