# Importing OR-Tools: The code starts by importing the necessary module from OR-Tools for solving linear programming problems.
from ortools.linear_solver import pywraplp

# Setting Parameters: Parameters such as maxPiecesPerHarvest, firstHarvestWeek, marge, minimumNumberOfPlants, maximumNumberOfPlants, minimumPlantweek, maximumPlantweek, demand, 
# and productieschema are defined. These parameters represent various constraints and data related to your problem.
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

# Defining the Function calculate_supply_demand: This function takes in all the parameters mentioned above. 
# It sets up and solves a linear programming problem to find the optimal planting schedule that minimizes the total number of starting cuttings while meeting the demand for each week.
def calculate_supply_demand(maxPiecesPerHarvest, firstHarvestWeek, marge, minimumNumberOfPlants, maximumNumberOfPlants, minimumPlantweek, maximumPlantweek, demand, productieschema):
    # Creating the Solver: The function creates a linear solver using OR-Tools.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return

    num_weeks = maximumPlantweek - minimumPlantweek + 1

    # Defining Variables: It defines decision variables for each planting week (plant_weeks) and the number of starting cuttings for each week (start_cuttings). 
    # These variables are used to represent whether to plant in a specific week and how many cuttings to start with.
    plant_weeks = [solver.BoolVar(f'plant_week_{w}') for w in range(minimumPlantweek, maximumPlantweek + 1)]
    start_cuttings = [solver.IntVar(minimumNumberOfPlants, maximumNumberOfPlants, f'start_cuttings_{w}') for w in range(minimumPlantweek, maximumPlantweek + 1)]

    # Setting Constraints: Constraints are added to ensure that the supply for each week meets or exceeds the demand. 
    # This is done by calculating the supply based on the starting cuttings and the growth percentage specified in the produtionscheme, and then comparing it with the demand for that week.
    for week in range(minimumPlantweek, maximumPlantweek + 1):
        supply = solver.IntVar(0, solver.infinity(), f'supply_{week}')
        harvest_week_sum = solver.Sum(
            start_cuttings[plant_week - minimumPlantweek] * productieschema.get(week - plant_week + 1 - firstHarvestWeek, 0) / 100 * maxPiecesPerHarvest
            for plant_week in range(minimumPlantweek, week - firstHarvestWeek + 2)
        )
        solver.Add(supply == harvest_week_sum)
        solver.Add(supply >= demand.get(week, 0) - margin)  # Relaxing the constraint to allow supply to be the margin above demand


    # Setting the Objective: The objective is to minimize the total number of starting cuttings. This is achieved by summing up the starting cuttings for each week and minimizing this sum.
    solver.Minimize(solver.Sum(start_cuttings[w - minimumPlantweek] for w in range(minimumPlantweek, maximumPlantweek + 1)))

    # Solving the Problem: The solver is instructed to minimize the objective function while satisfying the defined constraints.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal solutions found:')
        for w in range(num_weeks):
            if plant_weeks[w].solution_value() > 0:
                print(f'Planting week: {w + minimumPlantweek}, Start cuttings: {start_cuttings[w].solution_value()}')
    else:
        print('No optimal solution found.')

    # Final supply and updated demand
    final_supply = {week: 0 for week in range(minimumPlantweek, maximumPlantweek + 1)}
    for w in range(num_weeks):
        if plant_weeks[w].solution_value() > 0:
            for week in range(minimumPlantweek, maximumPlantweek + 1):
                growth_week = week - (w + minimumPlantweek) + 1
                if growth_week >= firstHarvestWeek:
                    percentage = productieschema.get(growth_week - firstHarvestWeek, 0) / 100
                    final_supply[week] += int(start_cuttings[w].solution_value() * percentage * maxPiecesPerHarvest)
                    
    # Outputting the Results: If an optimal solution is found, the function prints the optimal planting schedule (planting week and the corresponding number of starting cuttings). 
    # It also prints the final supply and updated demand for each week based on the optimal solution.
    print("\nFinal supply per sales week:")
    for week, supply_value in final_supply.items():
        print(f"Week {week}\t{supply_value}\tCuttings")

    print("\nFinal updated demand per sales week:")
    updated_demand = {week: demand[week] - final_supply[week] for week in demand}
    for week, demand_value in updated_demand.items():
        print(f"Week {week}\t{demand_value}\tCuttings")

calculate_supply_demand(maxPiecesPerHarvest, firstHarvestWeek, margin, minimumNumberOfPlants, maximumNumberOfPlants, minimumPlantweek, maximumPlantweek, demand, productieschema)











