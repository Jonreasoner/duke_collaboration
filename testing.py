from grid_world import create_grid_world, plot_grid_world
from astar_planner import get_trajectory
from scheduler_milp import get_schedule

grid, rooms = create_grid_world()


# ----- Setting up test case scheduler inputs ----- #
agents = ['human', 'robot']
task_durations = {
    'room_1': 5,
    'room_2': 5,
    'room_3': 5,
    'room_4': 10,
    'room_5': 10,
    'room_6': 10
}
initial_position = (75, 125)
final_position = initial_position

def get_baseline_setup():
    h_tasks = ['room_1', 'room_2', 'room_3', 'room_4']
    r_tasks = ['room_4', 'room_5', 'room_6']
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
            'lin_vel': 0.6,
            'current_pos': initial_position,
            'tasks': r_tasks
        }
    }
    return world_params, agent_params, task_params

def inject_robot_delay(schedule_human, schedule_robot, agent_params, task_params):
    # mapping from coordinates to room labels
    coord_to_label = {}
    for task_label, task_info in task_params.items():
        coord_to_label[task_info['location']] = task_label
    # Convert coordinate schedules to room labels (skip initial and final positions)
    schedule_human_labels = [coord_to_label.get(coord) for coord in schedule_human]
    schedule_robot_labels = [coord_to_label.get(coord) for coord in schedule_robot]
    # Filter just in case
    schedule_human_labels = [t for t in schedule_human_labels if t is not None]
    schedule_robot_labels = [t for t in schedule_robot_labels if t is not None]
    # get indices
    common_tasks = set(schedule_human_labels) & set(schedule_robot_labels)
    human_common_tasks_indeces = {task: schedule_human_labels.index(task) for task in common_tasks}
    robot_common_tasks_indeces = {task: schedule_robot_labels.index(task) for task in common_tasks}
    # Find the first common task (earliest in human's schedule)
    first_common_task = min(common_tasks, key=lambda t: human_common_tasks_indeces[t])
    first_common_task_location = task_params[first_common_task]['location']
    # Find the task the robot does before the common task
    first_common_task_robot_index = robot_common_tasks_indeces[first_common_task]
    robot_prev_task_index = first_common_task_robot_index - 1
    robot_prev_task = schedule_robot_labels[robot_prev_task_index]
    robot_prev_task_location = task_params[robot_prev_task]['location']
    # Store original end position before updating current_pos
    original_end_position = agent_params['human']['current_pos']
    # Update agent positions
    agent_params['human']['current_pos'] = first_common_task_location
    agent_params['robot']['current_pos'] = robot_prev_task_location
    # Keep end_positions as the original starting point for both
    agent_params['human']['end_pos'] = original_end_position
    agent_params['robot']['end_pos'] = (21, 174) # since slow, it needs to end here for this specific ex
    # Human keeps: common task and all tasks after it in their original assignment
    human_remaining_labels = set(schedule_human_labels[human_common_tasks_indeces[first_common_task]:])
    agent_params['human']['tasks'] = [t for t in agent_params['human']['tasks'] if t in human_remaining_labels]
    # Robot keeps: prev task, common task, and all tasks after common task in their original assignment
    robot_remaining_labels = set(schedule_robot_labels[robot_prev_task_index:])
    agent_params['robot']['tasks'] = [t for t in agent_params['robot']['tasks'] if t in robot_remaining_labels]
    # Update the robot's previous task duration to include long delay
    task_params[robot_prev_task]['duration'] += task_params[first_common_task]['duration'] + 100

    return agent_params, task_params


# -------- GET SCHEDULE -------- #
world_params, agent_params, task_params = get_baseline_setup()
schedules = get_schedule(world_params, agent_params, task_params)
schedule_human = schedules['human']
print("Schedule for human: ", schedule_human)
schedule_robot = schedules['robot']
print("Schedule for robot: ", schedule_robot)
# pause = input("Press Enter to continue...")

# -------- INJECT DELAY AND GET UPDATED SCHEDULE -------- #
agent_params, task_params = inject_robot_delay(schedule_human, schedule_robot, agent_params, task_params)
# print(f"\nAfter inject_robot_delay:")
# print(f"Human tasks: {agent_params['human']['tasks']}")
# print(f"Robot tasks: {agent_params['robot']['tasks']}")
updated_schedules = get_schedule(world_params, agent_params, task_params)
updated_schedule_human = updated_schedules['human']
print("Updated schedule for human: ", updated_schedule_human)
updated_schedule_robot = updated_schedules['robot']
print("Updated schedule for robot: ", updated_schedule_robot)



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