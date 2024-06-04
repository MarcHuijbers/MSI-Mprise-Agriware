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
        return None

    num_weeks = maximumPlantweek - minimumPlantweek + 1

    # Decision variables
    start_cuttings = [solver.IntVar(0, maximumNumberOfPlants, f'start_cuttings_{w}') for w in range(minimumPlantweek, maximumPlantweek + 1)]
    plant_job = [solver.BoolVar(f'plant_job_{w}') for w in range(minimumPlantweek, maximumPlantweek + 1)]

    # Constraints
    for week in range(minimumPlantweek, maximumPlantweek + 1):
        # Define the supply based on start cuttings and production schedule
        supply = solver.Sum(
            start_cuttings[plant_week - minimumPlantweek] * productieschema.get(week - plant_week + 1 - firstHarvestWeek, 0) / 100 * maxPiecesPerHarvest
            for plant_week in range(minimumPlantweek, week - firstHarvestWeek + 2)
        )
        # Ensure supply meets demand with margin
        solver.Add(supply >= demand.get(week, 0) - margin)
        # Ensure start cuttings are only planted if a planting job is done
        solver.Add(start_cuttings[week - minimumPlantweek] <= maximumNumberOfPlants * plant_job[week - minimumPlantweek])
        # Ensure minimum number of plants if planting job is done
        solver.Add(start_cuttings[week - minimumPlantweek] >= minimumNumberOfPlants * plant_job[week - minimumPlantweek])

    # Objective function: minimize the total number of starting cuttings and the number of planting jobs
    solver.Minimize(
        solver.Sum(start_cuttings[w - minimumPlantweek] for w in range(minimumPlantweek, maximumPlantweek + 1)) +
        solver.Sum(plant_job[w - minimumPlantweek] * 1000 for w in range(minimumPlantweek, maximumPlantweek + 1))  # Penalty factor for planting jobs
    )

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        optimal_schedule = {}
        for w in range(num_weeks):
            if start_cuttings[w].solution_value() > 0:
                optimal_schedule[w + minimumPlantweek] = start_cuttings[w].solution_value()
        
        print('Optimal planting schedule found:')
        for week, cuttings in optimal_schedule.items():
            print(f'Planting week: {week}, Start cuttings: {cuttings}')

        print('\nSupply vs Demand:')
        for week in range(minimumPlantweek, maximumPlantweek + 1):
            supply = sum(
                optimal_schedule.get(plant_week, 0) * productieschema.get(week - plant_week + 1 - firstHarvestWeek, 0) / 100 * maxPiecesPerHarvest
                for plant_week in range(minimumPlantweek, week - firstHarvestWeek + 2)
            )
            print(f'Week: {week}, Demand: {demand.get(week, 0)}, Supply: {supply}')
        
        return optimal_schedule
    else:
        print('No optimal solution found.')
        return None

optimal_schedule = calculate_optimal_planting_weeks(maxPiecesPerHarvest, firstHarvestWeek, margin, minimumNumberOfPlants, maximumNumberOfPlants, minimumPlantweek, maximumPlantweek, demand, productieschema)
print("\nOptimal Schedule Dictionary:", optimal_schedule)
