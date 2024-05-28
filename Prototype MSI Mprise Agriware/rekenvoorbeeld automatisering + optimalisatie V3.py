from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value, PULP_CBC_CMD

# Settings
maxPiecesPerHarvest = 5
firstHarvestWeek = 3
marge = 0.1  # Marge als fractie van de vraag

productieschema = {
    1: 20,
    2: 40,
    3: 60,
    4: 80,
    5: 100,
    6: 100,
    7: 100,
    8: 100,
    9: 100,
    10: 70,
    11: 40,
    12: 10
}
demand = {
    1: 0,
    2: 0,
    3: 0,
    4: 10,
    5: 20,
    6: 30,
    7: 90,
    8: 150,
    9: 200,
    10: 275,
    11: 350,
    12: 375,
    13: 385,
    14: 395,
    15: 380,
    16: 300,
    17: 225,
    18: 150,
    19: 88,
    20: 50,
    21: 13,
    22: 0,
    23: 0,
    24: 0,
    25: 0,
    26: 0,
    27: 0,
    28: 0,
    29: 0,
    30: 0,
    31: 0,
    32: 0
}

# Define the problem
problem = LpProblem("Cuttings_Planning_Optimization", LpMinimize)

# Decision variables: number of cuttings planted in each week
start_cuttings_vars = LpVariable.dicts("start_cuttings", range(1, 33), lowBound=0, cat='Integer')
planting_week_vars = LpVariable.dicts("planting_week", range(1, 33), lowBound=1, upBound=32, cat='Integer')

# Objective function: Minimize the number of start cuttings
problem += lpSum([start_cuttings_vars[week] for week in range(1, 33)])

# Constraints: Ensure that supply meets demand with a margin
for week in range(1, 33):
    supply = lpSum([start_cuttings_vars[w] * productieschema.get(week - value(planting_week_vars[w]) - firstHarvestWeek + 1, 0) / 100 * maxPiecesPerHarvest
                    for w in range(1, 33) if week - value(planting_week_vars[w]) + 1 >= firstHarvestWeek])
    problem += (supply >= (1 + marge) * demand[week])

# Solve the problem
solver = PULP_CBC_CMD(msg=True)
problem.solve(solver)

# Check if an optimal solution is found
if problem.status == 1:
    print("Optimal solution found!")
    for week in range(1, 33):
        if start_cuttings_vars[week].varValue > 0:
            print(f"Week {week}: Plant {start_cuttings_vars[week].varValue} cuttings")
else:
    print("No optimal solution found.")
