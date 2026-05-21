"""
grid_world.py

Creates a 200 x 200 occupancy-grid world with:
- 8 rooms total, 4 stacked vertically on the left and 4 stacked vertically on the right
- open doorways from each room into the central area
- 2 central obstacle blocks that also act as view occluders

Coordinate convention:
    point = (x, y)
    grid[y, x] = 0 means free
    grid[y, x] = 1 means occupied/wall/obstacle

Run directly:
    python grid_world.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pprint import pprint
from typing import Dict, List, Tuple, Optional

import numpy as np

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
except ImportError:  # plotting is optional
    plt = None


FREE = 0
OCCUPIED = 1
Point = Tuple[int, int]
Bounds = Tuple[int, int, int, int]  # x_min, y_min, x_max, y_max inclusive


@dataclass(frozen=True)
class WorldConfig:
    width: int = 200
    height: int = 200
    wall_thickness: int = 3
    border_thickness: int = 3
    left_room_wall_x: int = 42
    right_room_wall_x: int = 156
    door_height: int = 16


def _paint_rect(grid: np.ndarray, x0: int, y0: int, x1: int, y1: int, value: int) -> None:
    """Paint an inclusive rectangle into the occupancy grid."""
    h, w = grid.shape
    x0 = max(0, min(w - 1, int(x0)))
    x1 = max(0, min(w - 1, int(x1)))
    y0 = max(0, min(h - 1, int(y0)))
    y1 = max(0, min(h - 1, int(y1)))
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0
    grid[y0 : y1 + 1, x0 : x1 + 1] = value


def create_grid_world(config: Optional[WorldConfig] = None) -> Tuple[np.ndarray, Dict[str, dict]]:
    """
    Build the grid world and return the occupancy grid plus a room dictionary.

    Returns
    -------
    grid : np.ndarray
        Shape (height, width). 0 is free, 1 is occupied.
    rooms : dict
        Each room has:
            center: coordinate the robot can navigate to for that room
            doorway: coordinate inside the doorway from the central area
            bounds: inclusive room bounds as (x_min, y_min, x_max, y_max)
            side: 'left' or 'right'
    """
    cfg = config or WorldConfig()
    grid = np.zeros((cfg.height, cfg.width), dtype=np.uint8)

    wt = cfg.wall_thickness
    bt = cfg.border_thickness
    lx = cfg.left_room_wall_x
    rx = cfg.right_room_wall_x

    # Outer boundary walls.
    _paint_rect(grid, 0, 0, cfg.width - 1, bt - 1, OCCUPIED)
    _paint_rect(grid, 0, cfg.height - bt, cfg.width - 1, cfg.height - 1, OCCUPIED)
    _paint_rect(grid, 0, 0, bt - 1, cfg.height - 1, OCCUPIED)
    _paint_rect(grid, cfg.width - bt, 0, cfg.width - 1, cfg.height - 1, OCCUPIED)

    # Vertical walls separating side rooms from the central hall.
    _paint_rect(grid, lx, 0, lx + wt - 1, cfg.height - 1, OCCUPIED)
    _paint_rect(grid, rx, 0, rx + wt - 1, cfg.height - 1, OCCUPIED)

    # Horizontal dividers within the left and right room stacks.
    # These do not extend through the central region.
    divider_ys = [50, 100, 150]
    for y in divider_ys:
        _paint_rect(grid, 0, y, lx + wt - 1, y + wt - 1, OCCUPIED)
        _paint_rect(grid, rx, y, cfg.width - 1, y + wt - 1, OCCUPIED)

    # Door openings in the vertical separator walls.
    room_bands = [(bt, 49), (52, 99), (102, 149), (152, cfg.height - bt - 1)]
    door_half = cfg.door_height // 2
    rooms: Dict[str, dict] = {}

    for idx, (y0, y1) in enumerate(room_bands, start=1):
        cy = (y0 + y1) // 2
        dy0 = cy - door_half
        dy1 = cy + door_half - 1

        # Left doorway through the left separator wall.
        _paint_rect(grid, lx, dy0, lx + wt - 1, dy1, FREE)
        rooms[f"room_{idx}"] = {
            "center": (lx // 2, cy),
            "doorway": (lx + wt, cy),
            "bounds": (bt, y0, lx - 1, y1),
            "side": "left",
        }

        # Right doorway through the right separator wall.
        _paint_rect(grid, rx, dy0, rx + wt - 1, dy1, FREE)
        rooms[f"room_{idx + 4}"] = {
            "center": ((rx + wt + cfg.width - bt - 1) // 2, cy),
            "doorway": (rx - 1, cy),
            "bounds": (rx + wt, y0, cfg.width - bt - 1, y1),
            "side": "right",
        }

    # Two central obstacle/occlusion blocks.
    # Stored in the grid as occupied cells, so A* avoids them and visibility checks can treat them as blockers.
    _paint_rect(grid, 84, 36, 122, 82, OCCUPIED)
    _paint_rect(grid, 84, 118, 122, 164, OCCUPIED)

    return grid, rooms


def get_room_targets(rooms: Dict[str, dict]) -> Dict[str, Point]:
    """Return the simple command dictionary: room name -> navigation target."""
    return {name: info["center"] for name, info in rooms.items()}


def is_free(grid: np.ndarray, point: Point) -> bool:
    """Return True if point is inside the grid and not occupied."""
    x, y = point
    return 0 <= y < grid.shape[0] and 0 <= x < grid.shape[1] and grid[y, x] == FREE


def line_of_sight_cells(start: Point, end: Point) -> List[Point]:
    """
    Integer grid cells crossed by a line from start to end, using Bresenham's algorithm.
    Useful later for checking whether the two central obstacle blocks occlude view.
    """
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    cells: List[Point] = []
    x, y = x0, y0
    while True:
        cells.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy
    return cells


def has_line_of_sight(grid: np.ndarray, start: Point, end: Point) -> bool:
    """
    Return True when the straight segment from start to end does not cross occupied cells.
    Boundary walls and the two central obstacle blocks all count as occluders.
    """
    for x, y in line_of_sight_cells(start, end):
        if not (0 <= y < grid.shape[0] and 0 <= x < grid.shape[1]):
            return False
        if grid[y, x] == OCCUPIED:
            return False
    return True


def plot_grid_world(
    grid: np.ndarray,
    rooms: Dict[str, dict],
    path: Optional[List[Point]] = None,
    start: Optional[Point] = None,
    goal: Optional[Point] = None,
    save_path: Optional[str] = None,
    show: bool = True,
) -> None:
    """Plot the grid, room centers, optional start/goal, and optional A* path."""
    if plt is None:
        raise ImportError("matplotlib is required for plotting. Install it with: pip install matplotlib")

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(grid, cmap="Greys", origin="upper", interpolation="nearest")

    for name, info in rooms.items():
        cx, cy = info["center"]
        dx, dy = info["doorway"]
        ax.scatter(cx, cy, marker="o", s=35)
        ax.scatter(dx, dy, marker="s", s=20)
        ax.text(cx + 2, cy - 2, name, fontsize=8)

    if path:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        ax.plot(xs, ys, linewidth=2)

    if start is not None:
        ax.scatter(start[0], start[1], marker="x", s=80, label="start")
    if goal is not None:
        ax.scatter(goal[0], goal[1], marker="*", s=100, label="goal")

    ax.set_title("200 x 200 Grid World")
    ax.set_xlabel("x cell")
    ax.set_ylabel("y cell")
    ax.set_xlim(-1, grid.shape[1])
    ax.set_ylim(grid.shape[0], -1)
    ax.set_aspect("equal")
    ax.grid(True, linewidth=0.2, alpha=0.3)
    if start is not None or goal is not None:
        ax.legend(loc="upper right")
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=200)
    if show:
        plt.show()
    else:
        plt.close(fig)


def main() -> None:
    grid, rooms = create_grid_world()
    room_targets = get_room_targets(rooms)

    print("Grid shape:", grid.shape)
    print("Cell convention: grid[y, x], 0=free, 1=occupied")
    print("\nRoom target dictionary:")
    pprint(room_targets)

    # Save a figure by default so you can inspect the generated map without needing a GUI.
    plot_grid_world(grid, rooms, save_path="grid_world_design.png", show=True)


if __name__ == "__main__":
    main()
