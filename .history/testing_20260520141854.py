from grid_world import create_grid_world
from astar_planner import get_trajectory

grid, rooms = create_grid_world()

initial_position = (75, 125)
final_position = initial_position
room_1 = rooms["room_1"]["center"]
room_2 = rooms["room_2"]["center"]
room_3 = rooms["room_3"]["center"]
room_4 = rooms["room_4"]["center"]
room_5 = rooms["room_5"]["center"]
room_6 = rooms["room_6"]["center"]
room_7 = rooms["room_7"]["center"]
room_8 = rooms["room_8"]["center"]

schedule = [initial_position, room_1, room_2, room_3, room_4, room_5, room_6, room_7, room_8, final_position]
for i in range(len(schedule) - 1):
    start_position = schedule[i]
    end_position = schedule[i + 1]
    trajectory = get_trajectory(
        start_position=start_position,
        end_position=end_position,
        grid=grid,
        rooms=rooms,
        allow_diagonal=True,
        waypoint_stride=10,
    )
    print(f"Trajectory from {start_position} to {end_position}:")
    print("Sparse waypoints:")
    print(trajectory["waypoints"])
    print("Path length:")
    print(trajectory["path_length"])


# print("rooms: ", rooms)
# start_position = (100, 100)
# start_position = (rooms["room_8"]["center"])
# end_position = rooms["room_1"]["center"]

# trajectory = get_trajectory(
#     start_position=start_position,
#     end_position=end_position,
#     grid=grid,
#     rooms=rooms,
#     allow_diagonal=True,
#     waypoint_stride=10,
# )

# print("Sparse waypoints:")
# print(trajectory["waypoints"])

# print("Path length:")
# print(trajectory["path_length"])
print('DONE')