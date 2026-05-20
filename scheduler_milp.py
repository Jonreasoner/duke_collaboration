'''MILP for nurse and robot scheduling'''

import gurobipy as gp
from gurobipy import GRB

# ----------------------------------------------------- SCHEDULE FUNCTION ----------------------------------------------------- #


def get_schedule(world_params, agent_params, task_params):
    # ----- EXTRACT PARAMS ----- #
    agents = world_params['agents']
    all_tasks = sorted(task_params.keys())
    task_durations = {task: task_params[task]['duration'] for task in all_tasks}
    task_locations = {task: task_params[task]['location'] for task in all_tasks}
    task_agents = {task: task_params[task]['agents'] for task in all_tasks}
    h_lin_vel = agent_params['nurse']['lin_vel']
    r_lin_vel = agent_params['robot']['lin_vel']


    # ----- VARIABLES ----- #
    model = gp.Model("HR_Scheduling")
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
        # 1. one start / end node
        model.addConstr(gp.quicksum(start_node[task, agent] for task in all_tasks) == 1, name=f"one_start_{agent}")
        model.addConstr(gp.quicksum(end_node[task, agent] for task in all_tasks) == 1, name=f"one_end_{agent}")
        # 2. start / end path handling
        for j in all_tasks:

            model.addConstr(x[j, j, agent] == 0, name=f"no_self_loop_{j}_{agent}")

            if j in agent_tasks[agent]: # if this task is assigned to agent
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
                    travel_time = ((task_locations[i][0] - task_locations[j][0])**2 + (task_locations[i][1] - task_locations[j][1])**2)**0.5 / (h_lin_vel if agent == 'nurse' else r_lin_vel)
                    model.addConstr(t_s[j] >= t_s[i] + task_durations[i] + travel_time - big_M * (1 - x[i, j, agent]), name=f"timeline_{i}_{j}_{agent}")

            # 5. makespan definition
            model.addConstr(T_f >= t_s[j] + task_durations[j] - big_M * (1 - end_node[j, agent]), name=f"makespan_{j}_{agent}")


    # ----- OBJECTIVE ----- #
    model.setObjective(T_f, GRB.MINIMIZE)
    model.optimize()

    # ----- BUILD COMPATIBLE OUTPUT WITH REST OF SIM ----- # 
    output_schedule = {agent: {} for agent in agents}

    if model.status == GRB.OPTIMAL:
        # print(f"\nOptimal Solution Found! Total Makespan: {T_f.X:.2f} seconds.\n")
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

                output_schedule[agent][step] = {
                    'task': current_task,
                    'arrival': round(start_val, 2), # right now, the agent essentially waits at the last task, but I can edit that in a bit
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
        import pprint
        pprint.pprint(output_schedule)
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
agents = ['nurse', 'robot']
h_start = (1, 1)
r_start = (19, 19)

# ----- TASK INIT ----- #
'''
Nurse will have 4 tasks / patients to visit
Robot will have 3 tasks / meds to deliver
One task will overlap, where nurse need the medicine to administer
'''
h_tasks = ['A', 'B', 'C', 'D']
r_tasks = ['D', 'E', 'F']
agent_tasks = {
    'nurse': h_tasks,
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
    'nurse': {
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
