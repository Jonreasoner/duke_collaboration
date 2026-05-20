from grid_world import create_grid_world
from astar_planner import get_trajectory

grid, rooms = create_grid_world()
print("rooms: ", rooms)
start_position = (100, 100)
end_position = rooms["room_1"]["center"]

trajectory = get_trajectory(
    start_position=start_position,
    end_position=end_position,
    grid=grid,
    allow_diagonal=False,
    waypoint_stride=10,
)

print("Sparse waypoints:")
print(trajectory["waypoints"])

print("Path length:")
print(trajectory["path_length"])