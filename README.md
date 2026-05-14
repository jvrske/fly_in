*This project has been created as part of the 42 curriculum by csilva.*

# Fly-in

## Description

Fly-in is a drone routing simulation system that navigates a fleet of drones from a
start zone to an end zone through a weighted graph network. The system parses a custom
map format, builds a graph of connected zones, finds the optimal path using Dijkstra's
algorithm, and simulates all drone movements turn by turn while respecting zone
capacity, connection capacity, and movement cost constraints.

Zone types supported:
- **normal** – 1 turn movement cost (default)
- **restricted** – 2 turn movement cost (drone occupies the connection during transit)
- **priority** – 1 turn movement cost, preferred by the pathfinding algorithm
- **blocked** – inaccessible, ignored by the algorithm

## Instructions

### Requirements

- Python 3.10 or later
- pip

### Installation

Install all dependencies:

```bash
make install
```

### Running the simulation

```bash
make run
```

Or directly, passing a map file as argument:

```bash
python3 fly_in.py maps/easy/01_linear_path.txt
```

### Visual mode

Add the `--visual` flag to enable colored terminal output:

```bash
python3 fly_in.py maps/easy/01_linear_path.txt --visual
```

### Debug mode

Run the simulation with Python's built-in debugger:

```bash
make debug
```

### Lint

Run flake8 and mypy checks:

```bash
make lint
```

### Clean

Remove cache files:

```bash
make clean
```

### Available maps

```
maps/easy/01_linear_path.txt
maps/easy/02_simple_fork.txt
maps/easy/03_basic_capacity.txt
maps/medium/01_dead_end_trap.txt
maps/medium/02_circular_loop.txt
maps/medium/03_priority_puzzle.txt
maps/hard/01_maze_nightmare.txt
maps/hard/02_capacity_hell.txt
maps/hard/03_ultimate_challenge.txt
maps/challenger/01_the_impossible_dream.txt
```

## Algorithm

The pathfinding is implemented using **Dijkstra's algorithm** with weighted edges
based on zone types. Each hub has a `movement_cost` derived from its zone type
(normal/priority = 1, restricted = 2, blocked = excluded). The algorithm finds the
single shortest path from start to end and assigns it to all drones.

**Simulation mechanics:**
- Drones are processed sequentially (D1 before D2, etc.) each turn
- A drone moving out of a zone frees its capacity in that same turn, enabling
  pipelining through bottlenecks
- Restricted zones use a 2-turn transit mechanic: on turn 1 the drone enters the
  connection (in-transit state); on turn 2 it must arrive at the destination
- Edge and zone capacity constraints are checked before committing any move
- If no drone can move and not all have arrived, a deadlock is detected and reported

**Complexity:**
- Dijkstra: O((V + E) log V) where V = number of zones, E = number of connections
- Simulation: O(T × N) where T = total turns, N = number of drones
- Paths are computed once and cached — no recalculation during simulation

## Visual Representation

When running with `--visual`, each drone ID is printed in **bold** and each zone name
is printed in its configured color from the map metadata. Colors are mapped to ANSI
256-color terminal escape codes, supporting values such as `red`, `blue`, `green`,
`orange`, `purple`, `cyan`, `yellow`, `magenta`, `lime`, `crimson`, and `rainbow`
(per-character color cycling).

Drones in transit toward a restricted zone are displayed as `D<ID>-<source>><dest>`,
showing the connection being traversed.

## Resources

- [Dijkstra's Algorithm – Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python heapq documentation](https://docs.python.org/3/library/heapq.html)
- [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)
- [mypy documentation](https://mypy.readthedocs.io/)

**AI usage:** Claude (Anthropic) was used to assist with debugging type annotation
errors caught by mypy, fixing runtime bugs in the restricted zone transit mechanic,
and implementing the ANSI color visual output. All generated code was reviewed,
tested, and understood before being integrated into the project.
