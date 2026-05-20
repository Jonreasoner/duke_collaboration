"""
astar_planner.py

A* planner for the 200 x 200 grid world created in grid_world.py.

Coordinate convention:
    point = (x, y)
    grid[y, x] = 0 means free
    grid[y, x] = 1 means occupied/wall/obstacle

Example:
    from grid_world import create_grid_world
    from astar_planner import astar, plan_to_room

    grid, rooms = create_grid_world()
    start = (100, 100)
    path = plan_to_room(start, "room_1", grid, rooms)
"""

from __future__ import annotations

import heapq
import math
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np

Point = Tuple[int, int]


class NoPathError(RuntimeError):
    """Raised when A* cannot find a valid path."""


def in_bounds(grid: np.ndarray, point: Point) -> bool:
    x, y = point
    return 0 <= y < grid.shape[0] and 0 <= x < grid.shape[1]


def is_free(grid: np.ndarray, point: Point) -> bool:
    x, y = point
    return in_bounds(grid, point) and grid[y, x] == 0


def neighbors_4(point: Point) -> Iterable[Tuple[Point, float]]:
    x, y = point
    yield (x + 1, y), 1.0
    yield (x - 1, y), 1.0
    yield (x, y + 1), 1.0
    yield (x, y - 1), 1.0


def neighbors_8(point: Point) -> Iterable[Tuple[Point, float]]:
    x, y = point
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            cost = math.sqrt(2.0) if dx != 0 and dy != 0 else 1.0
            yield (x + dx, y + dy), cost


def heuristic(a: Point, b: Point, allow_diagonal: bool = False) -> float:
    """Admissible A* heuristic for 4- or 8-connected motion."""
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    if allow_diagonal:
        # Octile distance.
        return max(dx, dy) + (math.sqrt(2.0) - 1.0) * min(dx, dy)
    return float(dx + dy)


def _diagonal_move_is_valid(grid: np.ndarray, current: Point, nxt: Point) -> bool:
    """
    Prevent diagonal corner-cutting through obstacle corners.
    Example: moving from (x,y) to (x+1,y+1) is only allowed if both side cells are free.
    """
    cx, cy = current
    nx, ny = nxt
    dx = nx - cx
    dy = ny - cy
    if abs(dx) != 1 or abs(dy) != 1:
        return True
    return is_free(grid, (cx + dx, cy)) and is_free(grid, (cx, cy + dy))


def reconstruct_path(came_from: Dict[Point, Point], current: Point) -> List[Point]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def astar(
    grid: np.ndarray,
    start: Point,
    goal: Point,
    allow_diagonal: bool = False,
) -> List[Point]:
    """
    Compute an A* path from start to goal.

    Parameters
    ----------
    grid : np.ndarray
        Occupancy grid. 0 is free, nonzero is occupied.
    start : tuple[int, int]
        Start coordinate as (x, y).
    goal : tuple[int, int]
        Goal coordinate as (x, y).
    allow_diagonal : bool
        If False, use 4-connected movement. If True, use 8-connected movement.

    Returns
    -------
    list[tuple[int, int]]
        Path from start to goal, inclusive.
    """
    start = (int(start[0]), int(start[1]))
    goal = (int(goal[0]), int(goal[1]))

    if not is_free(grid, start):
        raise ValueError(f"Start {start} is outside the grid or occupied.")
    if not is_free(grid, goal):
        raise ValueError(f"Goal {goal} is outside the grid or occupied.")

    neighbor_fn = neighbors_8 if allow_diagonal else neighbors_4

    # Priority queue entries: (estimated_total_cost, cost_so_far, node)
    open_heap: List[Tuple[float, float, Point]] = []
    heapq.heappush(open_heap, (heuristic(start, goal, allow_diagonal), 0.0, start))

    came_from: Dict[Point, Point] = {}
    g_score: Dict[Point, float] = {start: 0.0}
    closed: set[Point] = set()

    while open_heap:
        _, current_cost, current = heapq.heappop(open_heap)

        # Skip stale queue entries.
        if current in closed:
            continue
        closed.add(current)

        if current == goal:
            return reconstruct_path(came_from, current)

        for nxt, step_cost in neighbor_fn(current):
            if not is_free(grid, nxt):
                continue
            if allow_diagonal and not _diagonal_move_is_valid(grid, current, nxt):
                continue
            if nxt in closed:
                continue

            tentative_g = current_cost + step_cost
            if tentative_g < g_score.get(nxt, math.inf):
                came_from[nxt] = current
                g_score[nxt] = tentative_g
                f_score = tentative_g + heuristic(nxt, goal, allow_diagonal)
                heapq.heappush(open_heap, (f_score, tentative_g, nxt))

    raise NoPathError(f"No path found from {start} to {goal}.")


def plan_to_room(
    current_location: Point,
    room_name: str,
    grid: np.ndarray,
    rooms: Dict[str, dict],
    allow_diagonal: bool = False,
) -> List[Point]:
    """
    Plan from the current robot location to the center coordinate of a named room.

    Example command mapping:
        go_to room_1 -> rooms["room_1"]["center"]
    """
    if room_name not in rooms:
        valid = ", ".join(sorted(rooms.keys()))
        raise KeyError(f"Unknown room '{room_name}'. Valid rooms are: {valid}")

    goal = tuple(rooms[room_name]["center"])
    return astar(grid, current_location, goal, allow_diagonal=allow_diagonal)


def path_length(path: List[Point]) -> float:
    """Return geometric length of a grid path."""
    if len(path) < 2:
        return 0.0
    total = 0.0
    for p0, p1 in zip(path[:-1], path[1:]):
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        total += math.hypot(dx, dy)
    return total


def sparsify_path(path: List[Point], stride: int = 5) -> List[Point]:
    """
    Downsample a dense cell-by-cell path for use as a simple waypoint trajectory.
    The final goal is always preserved. Useful because apparently robots prefer
    not receiving 300 individual micromanagement commands from a list.
    """
    if stride <= 1 or len(path) <= 2:
        return path
    sparse = path[::stride]
    if sparse[-1] != path[-1]:
        sparse.append(path[-1])
    return sparse


def main() -> None:
    from grid_world import create_grid_world, plot_grid_world

    grid, rooms = create_grid_world()

    start = (100, 100)
    room_name = "room_1"
    path = plan_to_room(start, room_name, grid, rooms, allow_diagonal=False)
    sparse_waypoints = sparsify_path(path, stride=8)

    print(f"Planning command: go_to {room_name}")
    print(f"Start: {start}")
    print(f"Goal:  {rooms[room_name]['center']}")
    print(f"Dense path cells: {len(path)}")
    print(f"Path length: {path_length(path):.2f} cells")
    print(f"Sparse waypoint trajectory ({len(sparse_waypoints)} waypoints):")
    print(sparse_waypoints)

    plot_grid_world(
        grid,
        rooms,
        path=path,
        start=start,
        goal=rooms[room_name]["center"],
        save_path="astar_path_demo.png",
        show=True,
    )


if __name__ == "__main__":
    main()
