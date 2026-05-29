'''MILP for human and robot scheduling'''

import numpy as np
import gurobipy as gp
from gurobipy import GRB
import pandas as pd

# ----------------------------------------------------- SCHEDULE EXTRACTION ----------------------------------------------------- #

def get_schedule(world_params, agent_params, task_params):
    
    output_schedule = build_schedule(world_params, agent_params, task_params)

    agent_schedules = {}
    for agent, params in agent_params.items():
        # Use end_pos if it's been set, otherwise use current_pos as the end position
        end_pos = params.get('end_pos', params['current_pos'])
        agent_schedules[agent] = per_agent(output_schedule, 
                                           agent, 
                                           start_position=params['current_pos'], 
                                           end_position=end_pos)

    return agent_schedules

def per_agent(output_schedule, agent, start_position=None, end_position=None):
    agent_schedule = []
    if start_position is not None:
        agent_schedule.append(start_position)

    agent_steps = output_schedule.get(agent, {})
    for step in sorted(agent_steps):
        agent_schedule.append(agent_steps[step]["location"])
    if end_position is not None:
        agent_schedule.append(end_position)

    return agent_schedule

# ----------------------------------------------------- SCHEDULE OPTIMIZATION ----------------------------------------------------- #


def build_schedule(world_params, agent_params, task_params):
    # ----- EXTRACT PARAMS ----- #
    agents = world_params['agents']
    all_tasks = sorted(task_params.keys())

    task_durations = {task: task_params[task]['duration'] for task in all_tasks}
    task_locations = {task: task_params[task]['location'] for task in all_tasks}
    task_agents = {task: task_params[task]['agents'] for task in all_tasks}

    h_lin_vel = agent_params['human']['lin_vel']
    r_lin_vel = agent_params['robot']['lin_vel']
    start_positions = {agent: agent_params[agent]['current_pos'] for agent in agents}
    # Use end_pos if set, otherwise use current_pos
    end_positions = {agent: agent_params[agent].get('end_pos', agent_params[agent]['current_pos']) for agent in agents}

    big_M = 1e6 # large constant for big-M method in constraints


    # ----- VARIABLES ----- #
    model = gp.Model("HR_Scheduling")
    model.setParam('OutputFlag', 0) # suppress Gurobi output

    ## Routing - x[i->j, a]##
    x = model.addVars(all_tasks, all_tasks, agents, vtype=GRB.BINARY, name="x")
    ## Start Var - s[i, a] ##
    start_node = model.addVars(all_tasks, agents, vtype=GRB.BINARY, name="start")
    ## End Var - e[i, a] ##
    end_node = model.addVars(all_tasks, agents, vtype=GRB.BINARY, name="end")
    ## Var Start Time ##
    t_s = model.addVars(all_tasks, vtype=GRB.CONTINUOUS, lb = 0.0, name="t_s")
    ## Makespan ##
    T_f = model.addVar(vtype=GRB.CONTINUOUS, lb = 0.0, name="T_f")

    # ----- CONSTRAINTS ----- #
    '''
    1. one start / end node
    2. .... need a way to handle start / end paths ....
    3. only select tasks that are assigned to the agent
    4. timeline continuity
    5. makespan definition
    '''
    for agent in agents:
        agent_task_list = agent_params[agent]['tasks']
        # 1. one start / end node
        model.addConstr(gp.quicksum(start_node[task, agent] for task in all_tasks) == 1, name=f"one_start_{agent}")
        model.addConstr(gp.quicksum(end_node[task, agent] for task in all_tasks) == 1, name=f"one_end_{agent}")
        
        start_travels = gp.quicksum(((task_locations[task][0] - start_positions[agent][0])**2 + (task_locations[task][1] - start_positions[agent][1])**2)**0.5 / (h_lin_vel if agent == 'human' else r_lin_vel) * start_node[task, agent] for task in all_tasks)
        end_travels = gp.quicksum(((task_locations[task][0] - end_positions[agent][0])**2 + (task_locations[task][1] - end_positions[agent][1])**2)**0.5 / (h_lin_vel if agent == 'human' else r_lin_vel) * end_node[task, agent] for task in all_tasks)
                                                                                             
        # 2. start / end path handling
        for j in all_tasks:

            model.addConstr(x[j, j, agent] == 0, name=f"no_self_loop_{j}_{agent}") 

            if j in agent_task_list: # if this task is assigned to agent
                model.addConstr((gp.quicksum(x[i, j, agent] for i in all_tasks if i != j) + start_node[j, agent] == 1), name=f"start_path_{j}_{agent}")
                model.addConstr((gp.quicksum(x[j, i, agent] for i in all_tasks if i != j) + end_node[j, agent] == 1), name=f"end_path_{j}_{agent}")
            # 3. only select tasks that are assigned to the agent
            else:
                model.addConstr(start_node[j, agent] == 0, name=f"no_start_{j}_{agent}")
                model.addConstr(end_node[j, agent] == 0, name=f"no_end_{j}_{agent}")
                model.addConstr((gp.quicksum(x[i, j, agent] for i in all_tasks) + start_node[j, agent] == 0), name=f"start_path_{j}_{agent}")
                model.addConstr((gp.quicksum(x[j, i, agent] for i in all_tasks) + end_node[j, agent] == 0), name=f"end_path_{j}_{agent}")

            # 4. timeline continuity
            for i in all_tasks:
                if i != j:
                    travel_time = ((task_locations[i][0] - task_locations[j][0])**2 + (task_locations[i][1] - task_locations[j][1])**2)**0.5 / (h_lin_vel if agent == 'human' else r_lin_vel)
                    model.addConstr(t_s[j] >= t_s[i] + task_durations[i] + travel_time - big_M * (1 - x[i, j, agent]), name=f"timeline_{i}_{j}_{agent}")
            # if it is a start node, add travel time from start position
            travel_time_start = ((task_locations[j][0] - start_positions[agent][0])**2 + (task_locations[j][1] - start_positions[agent][1])**2)**0.5 / (h_lin_vel if agent == 'human' else r_lin_vel)
            model.addConstr(t_s[j] >= travel_time_start - big_M * (1 - start_node[j, agent]), name=f"timeline_start_{j}_{agent}")

            # 5. makespan definition
            model.addConstr(T_f >= t_s[j] + task_durations[j] - big_M * (1 - end_node[j, agent]) + end_travels, name=f"makespan_{j}_{agent}")


    # ----- OBJECTIVE ----- #
    model.setObjective(T_f, GRB.MINIMIZE)
    # model.setParam('MIPGap', 0.0)  # Testing
    model.setParam('TimeLimit', 60)  # 60 second timeout
    model.optimize()
    model.write("model_constraints.lp")
    model.write("solution.sol")

    # ----- BUILD COMPATIBLE OUTPUT WITH REST OF SIM ----- # 
    output_schedule = {agent: {} for agent in agents}

    if model.status == GRB.OPTIMAL:
        print(f"Optimal Solution Found! Makespan: {T_f.X:.2f} seconds")
        for agent in agents:
            
            current_task = None
            for task in all_tasks:
                if start_node[task, agent].X > 0.5:
                    current_task = task
                    break
            
            step = 1
            while current_task is not None:
                start_val = t_s[current_task].X
                end_val = start_val + task_durations[current_task]

                prev_end = start_val
                if step > 1:
                    prev_task_end = output_schedule[agent][step - 1]['end']
                    prev_task_location = output_schedule[agent][step - 1]['location']
                    travel_time = ((task_locations[current_task][0] - prev_task_location[0])**2 + (task_locations[current_task][1] - prev_task_location[1])**2)**0.5 / (h_lin_vel if agent == 'human' else r_lin_vel)
                    prev_end = prev_task_end + travel_time
                
                arrival = round(prev_end, 2)
                
                output_schedule[agent][step] = {
                    'task': current_task,
                    'arrival': arrival,
                    'wait': max(0.0, round(start_val - arrival, 2)),
                    'start': round(start_val, 2),
                    'end': round(end_val, 2),
                    'duration': task_durations[current_task],
                    'collab': 1 if len(task_agents[current_task]) > 1 else 0,
                    'location': task_locations[current_task]     
                }

                if end_node[current_task, agent].X > 0.5: 
                    current_task = None 
                else:
                    next_task = None
                    for task_j in all_tasks:
                        if x[current_task, task_j, agent].X > 0.5:
                            next_task = task_j
                            break
                    current_task = next_task
            
                step += 1
            
        #print("Output Schedule:")
        #import pprint
        #pprint.pprint(output_schedule)
        # for agent in agents:
        #     print(f"\n{agent}:")
        #     for step in sorted(output_schedule[agent].keys()):
        #         task_info = output_schedule[agent][step]
        #         print(f"  Step {step}:")
        #         print(f"    'task': {task_info['task']}")
        #         print(f"    'arrival': {task_info['arrival']}")
        #         print(f"    'wait': {task_info['wait']}")
        #         print(f"    'start': {task_info['start']}")
        #         print(f"    'end': {task_info['end']}")
        #         print(f"    'duration': {task_info['duration']}")
        #         print(f"    'collab': {task_info['collab']}")
        #         print(f"    'location': {task_info['location']}")

        # ---- For Verification: print the travel times between tasks ---- #
        h_travel = np.zeros((len(all_tasks) + 2, len(all_tasks) + 2))  # +2 for start and end positions
        r_travel = np.zeros((len(all_tasks) + 2, len(all_tasks) + 2))

        # Fill in the travel times for human
        h_start_pos = start_positions['human']
        h_end_pos = end_positions['human']
        for i, task_i in enumerate(['start'] + all_tasks + ['end']):
            for j, task_j in enumerate(['start'] + all_tasks + ['end']):
                if task_i == 'start':
                    pos_i = h_start_pos
                elif task_i == 'end':
                    pos_i = h_end_pos
                else:
                    pos_i = task_locations[task_i]

                if task_j == 'start':
                    pos_j = h_start_pos
                elif task_j == 'end':
                    pos_j = h_end_pos
                else:
                    pos_j = task_locations[task_j]

                travel_time = ((pos_i[0] - pos_j[0])**2 + (pos_i[1] - pos_j[1])**2)**0.5 / h_lin_vel
                h_travel[i, j] = travel_time

        # Fill in the travel times for robot
        r_start_pos = start_positions['robot']
        r_end_pos = end_positions['robot']
        for i, task_i in enumerate(['start'] + all_tasks + ['end']):
            for j, task_j in enumerate(['start'] + all_tasks + ['end']):
                if task_i == 'start':
                    pos_i = r_start_pos
                elif task_i == 'end':
                    pos_i = r_end_pos
                else:
                    pos_i = task_locations[task_i]

                if task_j == 'start':
                    pos_j = r_start_pos
                elif task_j == 'end':
                    pos_j = r_end_pos
                else:
                    pos_j = task_locations[task_j]

                travel_time = ((pos_i[0] - pos_j[0])**2 + (pos_i[1] - pos_j[1])**2)**0.5 / r_lin_vel
                r_travel[i, j] = travel_time

        # Add labels for the first column and row
        labels = ['start'] + all_tasks + ['end']
        h_travel_df = pd.DataFrame(h_travel, index=labels, columns=labels)
        r_travel_df = pd.DataFrame(r_travel, index=labels, columns=labels)

        # Print the travel time matrices in a pretty format
        # print("Human Travel Time Matrix:")
        # print(h_travel_df.to_string(index=True, header=True, justify='left'))
        # print("Robot Travel Time Matrix:")
        # print(r_travel_df.to_string(index=True, header=True, justify='left'))

    else:
        print("No optimal solution found.")
    
    return output_schedule


# ----------------------------------------------------- TESTING ----------------------------------------------------- #

# ----- MISSION PARAMS ----- #
big_M = 1e6
h_lin_vel = 1.0 # m/s
r_lin_vel = 1.0 # m/s

# ----- WORLD SETUP ----- #
grid_size = 20
agents = ['human', 'robot']
h_start = (1, 1)
r_start = (19, 19)

# ----- TASK INIT ----- #
'''
human will have 4 tasks / patients to visit
Robot will have 3 tasks / meds to deliver
One task will overlap, where human need the medicine to administer
'''
h_tasks = ['A', 'B', 'C', 'D']
r_tasks = ['D', 'E', 'F']
agent_tasks = {
    'human': h_tasks,
    'robot': r_tasks
}
all_tasks = sorted(list(set(h_tasks) | set(r_tasks)))
task_agents = {task: [] for task in all_tasks}
for agent_id, tasks in agent_tasks.items():
    for task in tasks:
        task_agents[task].append(agent_id)

# ----- TASK DURATIONS ----- #
task_durations = {
    'A': 30,
    'B': 20,
    'C': 25,
    'D': 15, 
    'E': 10,
    'F': 20
}

# ----- TASK LOCATIONS ----- #
task_locations = {
    'A': (2, 5),
    'B': (5, 10),
    'C': (10, 15),
    'D': (15, 8),
    'E': (18, 12),
    'F': (12, 18)
}

# ----- PARAM DICTS ----- #
world_params = {
    'grid_size': grid_size,
    'agents': agents
}

agent_params = {
    'human': {
        'lin_vel': h_lin_vel,
        'current_pos': h_start,
        'tasks': h_tasks
    },
    'robot': {
        'lin_vel': r_lin_vel,
        'current_pos': r_start,
        'tasks': r_tasks
    }
}

task_params = {}
for task in all_tasks:
    task_params[task] = {
        'duration': task_durations[task],
        'location': task_locations[task],
        'agents': task_agents[task]
    }
    


if __name__ == "__main__":
    schedule = get_schedule(world_params, agent_params, task_params)
    print("Final Schedule:")
    import pprint
    pprint.pprint(schedule)
