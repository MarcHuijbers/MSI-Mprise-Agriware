from ortools.linear_solver import pywraplp

# Parameters
maxPiecesPerHarvest = 5
firstHarvestWeek = 3
margin = 10
minimumNumberOfPlants = 10
maximumNumberOfPlants = 50
minimumPlantweek = 1
maximumPlantweek = 32

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

def calculate_optimal_planting_weeks(maxPiecesPerHarvest, firstHarvestWeek, margin, minimumNumberOfPlants, maximumNumberOfPlants, minimumPlantweek, maximumPlantweek, demand, productieschema):
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return

    num_weeks = maximumPlantweek - minimumPlantweek + 1

    # Decision variables
    start_cuttings = [solver.IntVar(0, maximumNumberOfPlants, f'start_cuttings_{w}') for w in range(minimumPlantweek, maximumPlantweek + 1)]

    # Constraints to ensure supply meets or exceeds demand
    for week in range(minimumPlantweek, maximumPlantweek + 1):
        supply = solver.Sum(
            start_cuttings[plant_week - minimumPlantweek] * productieschema.get(week - plant_week + 1 - firstHarvestWeek, 0) / 100 * maxPiecesPerHarvest
            for plant_week in range(minimumPlantweek, week - firstHarvestWeek + 2)
        )
        solver.Add(supply >= demand.get(week, 0) - margin)

    # Objective function: minimize the total number of starting cuttings
    solver.Minimize(solver.Sum(start_cuttings[w - minimumPlantweek] for w in range(minimumPlantweek, maximumPlantweek + 1)))

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal planting schedule found:')
        for w in range(num_weeks):
            if start_cuttings[w].solution_value() > 0:
                print(f'Planting week: {w + minimumPlantweek}, Start cuttings: {start_cuttings[w].solution_value()}')
    else:
        print('No optimal solution found.')

calculate_optimal_planting_weeks(maxPiecesPerHarvest, firstHarvestWeek, margin, minimumNumberOfPlants, maximumNumberOfPlants, minimumPlantweek, maximumPlantweek, demand, productieschema)