from grid_world import create_grid_world, plot_grid_world
from astar_planner import get_trajectory
from scheduler_milp import get_schedule

grid, rooms = create_grid_world()


# ----- Setting up test case scheduler inputs ----- #
agents = ['human', 'robot']
h_tasks = ['room_1', 'room_2', 'room_3', 'room_4']
r_tasks = ['room_4', 'room_5', 'room_6']
task_durations = {
    'room_1': 0,
    'room_2': 0,
    'room_3': 0,
    'room_4': 0,
    'room_5': 0,
    'room_6': 0
}
all_tasks = sorted(list(set(h_tasks) | set(r_tasks)))
initial_position = (75, 125)
final_position = initial_position

### build dictionaries ###
task_params = {}
for task in all_tasks:
    task_params[task] = {
        'duration': task_durations[task],
        'room_label': task,
        'location': rooms[task]["center"],
        'agents': [a for a in agents if task in (h_tasks if a == 'human' else r_tasks)],
    }
world_params = {
    'grid_size': grid.shape,
    'agents': agents
}
agent_params = {
    'human': {
        'lin_vel': 1.0,
        'current_pos': initial_position,
        'tasks': h_tasks
    },
    'robot': {
        'lin_vel': 1.0,
        'current_pos': initial_position,
        'tasks': r_tasks
    }
}


# -------- GET SCHEDULE -------- #
schedules = get_schedule(world_params, agent_params, task_params)
schedule_human = schedules['human']
print("Schedule for human: ", schedule_human)
schedule_robot = schedules['robot']
print("Schedule for robot: ", schedule_robot)
# pause = input("Press Enter to continue...")



#schedule_robot = [initial_position, room_1, room_2, room_3, room_4, room_5, room_6, room_7, room_8, final_position]
#schedule_human = [initial_position, room_8, room_7, room_6, room_5, room_4, room_3, room_2, room_1, final_position]

for i in range(len(schedule_robot) - 1):
    start_position = schedule_robot[i]
    end_position = schedule_robot[i + 1]
    trajectory = get_trajectory(
        start_position=start_position,
        end_position=end_position,
        grid=grid,
        rooms=rooms,
        allow_diagonal=True,
        waypoint_stride=100,
    )
    if i == 0:
        total_trajectory = trajectory
    else:
        total_trajectory["path"].extend(trajectory["path"][1:])  # Avoid duplicating the start point
        total_trajectory["waypoints"].extend(trajectory["waypoints"])
        total_trajectory["path_length"] += trajectory["path_length"]
    
    # print(f"Trajectory from {start_position} to {end_position}:")
    # print("Sparse waypoints:")
    # print(trajectory["waypoints"])
    # print("Path length:")
    # print(trajectory["path_length"])

plot_grid_world(
        grid,
        rooms,
        path=total_trajectory["path"],
        start=initial_position,
        goal=final_position,
        # save_path="astar_path_demo.png",
        show=True,
    )

print("Total path length for full schedule: {:.2f} cells".format(total_trajectory["path_length"]))

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