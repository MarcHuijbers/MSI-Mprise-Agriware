from pulp import LpMinimize, LpProblem, LpVariable, lpSum

# Settings
maxPiecesPerHarvest = 5
firstHarvestWeek = 3
marge = 0

productieschema = {
    1 : 20,
    2 : 40,
    3 : 60,
    4 : 80,
    5 : 100,
    6 : 100,
    7 : 100,
    8 : 100,
    9 : 100,
    10 : 70,
    11 : 40,
    12 : 10
}

demand = {
    1 : 0,
    2 : 0,
    3 : 0,
    4 : 10,
    5 : 20,
    6 : 30,
    7 : 90,
    8 : 150,
    9 : 200,
    10 : 275,
    11 : 350,
    12 : 375,
    13 : 385,
    14 : 395,
    15 : 380,
    16 : 300,
    17 : 225,
    18 : 150,
    19 : 88,
    20 : 50,
    21 : 13,
    22 : 0,
    23 : 0,
    24 : 0,
    25 : 0,
    26 : 0,
    27 : 0,
    28 : 0,
    29 : 0,
    30 : 0,
    31 : 0,
    32 : 0
}

# Probleeminstantie maken
probleem = LpProblem("Minimalisatie probleem", LpMinimize)

# Variabelen definiëren
start_cuttings_vars = LpVariable.dicts("start_cuttings", range(1, 33), lowBound=0, cat='Integer')
planting_week_vars = LpVariable.dicts("planting_week", range(1, 33), lowBound=1, upBound=12, cat='Integer')  # Initialize with default value of 1

# Doelfunctie specificeren
probleem += lpSum(start_cuttings_vars)

# Beperkingen toevoegen
for week in range(1, 33):
    planting_week = int(planting_week_vars[week].varValue)
    first_harvest_week = int(firstHarvestWeek)
    probleem += lpSum(start_cuttings_vars[week] * float(productieschema.get(week - planting_week - first_harvest_week + 1, 0)) / 100 * maxPiecesPerHarvest) >= demand[week] - marge

# Probleem oplossen
probleem.solve()

# Resultaten interpreteren
print("Optimale oplossing:")
for week in range(1, 33):
    print(f"Week {week}: {int(start_cuttings_vars[week].varValue)} startplanten, geplant in week {int(planting_week_vars[week].varValue)}")
