# Dit is de geautomatiseerde versie van het excel bestand: productie voorstel reken voorbeeld.
# De input hiervan moet handmatig ingevoerd worden in de terminal. Onderstaand is een testcase gegeven die overeenkomt met de testcase in het excel bestand.
# TODO: Optimaliseer de aanbodlijn met ORTools.

# Settings
maxPiecesPerHarvest = 5
# First harvest week after planting the cuttings
firstHarvestWeek = 3
# Marge between supply and demand
marge = 0
# Minimum and maximum number of plants for one batch
minimumNumberOfPlants = 10
maximumNumberOfPlants = 50

# Minimum and maximum planting week
minimumPlantweek = 1
maximumPlantweek = 52

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


def calculate_supply_demand(maxPiecesPerHarvest, firstHarvestWeek, marge, minimumNumberOfPlants, maximumNumberOfPlants, minimumPlantweek, maximumPlantweek):
    # Initialize the counter for the iterations
    iteration = 0

    # Step 4: Iterate until the demand is met for all weeks
    while any(demand >= marge for demand in demand.values()):
        # Increment the counter for the iterations
        iteration += 1
        
        # Step 1: Enter the number of starting cuttings and the planting week
        while True:
            start_cuttings = int(input("Enter the number of starting cuttings: ")) # input aanpassen naar brute force
            if start_cuttings < minimumNumberOfPlants or start_cuttings > maximumNumberOfPlants:
                print(f"Number of starting cuttings must be between {minimumNumberOfPlants} and {maximumNumberOfPlants}.")
            else:
                break

        while True:
            planting_week = int(input("Enter the week to start planting: ")) # input aanpassen naar brute force
            if planting_week < minimumPlantweek or planting_week > maximumPlantweek:
                print("Invalid week. Please enter a week between 1 and 52.")
            else:
                break
        
        # Step 2: Calculate the output for each week based on the productieschema
        supply = {}
        for week in range(min(demand.keys()), len(demand)):  # Loop over the weeks from the minimum key in demand to week 32
            # The growth week is the week after planting the cuttings
            growth_week = week - planting_week + 1  # Calculate the growth week (subtract planting week and add 1 because the first week is week 1). 
            if growth_week >= firstHarvestWeek:  # Check if it's time to harvest the cuttings
                percentage = productieschema.get(growth_week - firstHarvestWeek, 0) / 100  # Get the harvest percentage for this growth week
                supply[week] = int(start_cuttings * percentage * maxPiecesPerHarvest)  # Calculate the supply for this week based on the percentage and the maximum pieces per harvest
            else:
                supply[week] = 0  # No supply before the first harvest week

        # Print the output for each week
        print()
        print(f"Iteration: {iteration}")
        print("Supply per sales week for the initial batch")
        for week, supply_value in supply.items():
            print(f"Week {week}\t{supply_value}\tCuttings")
            

        # Step 3: Update the demand per week based on the supply
        for week, demand_value in demand.items():
            demand[week] -= supply.get(week, 0)
            
        # Print the updated demand per week
        print()
        print(f"Iteration: {iteration}")
        print("Updated demand per sales week")
        for week, demand_value in demand.items():
            print(f"Week {week}\t{demand_value}\tCuttings")
            


calculate_supply_demand(maxPiecesPerHarvest, firstHarvestWeek, marge, minimumNumberOfPlants, maximumNumberOfPlants, minimumPlantweek, maximumPlantweek)

# Testcase 1 volgens Productie voorstel reken voorbeeld.
# Input:
# Enter the number of starting cuttings: 10
# Enter the week to start planting: 1 

# Expected output:
# Iteration: 1
# Supply per sales week for the initial batch
# Week 1  0       Cuttings
# Week 2  0       Cuttings
# Week 3  0.0     Cuttings
# Week 4  10.0    Cuttings
# Week 5  20.0    Cuttings
# Week 6  30.0    Cuttings
# Week 7  40.0    Cuttings
# Week 8  50.0    Cuttings
# Week 9  50.0    Cuttings
# Week 10 50.0    Cuttings
# Week 11 50.0    Cuttings
# Week 12 50.0    Cuttings
# Week 13 35.0    Cuttings
# Week 14 20.0    Cuttings
# Week 15 5.0     Cuttings
# Week 16 0.0     Cuttings
# Week 17 0.0     Cuttings


# Iteration: 1
# Updated demand per sales week
# Week 1  0       Cuttings
# Week 2  0       Cuttings
# Week 3  0.0     Cuttings
# Week 4  0.0     Cuttings
# Week 5  0.0     Cuttings
# Week 6  0.0     Cuttings
# Week 7  50.0    Cuttings
# Week 8  100.0   Cuttings
# Week 9  150.0   Cuttings
# Week 10 225.0   Cuttings
# Week 11 300.0   Cuttings
# Week 12 325.0   Cuttings
# Week 13 350.0   Cuttings
# Week 14 375.0   Cuttings
# Week 15 375.0   Cuttings
# Week 16 300.0   Cuttings
# Week 17 225.0   Cuttings
# Week 18 150.0   Cuttings
# Week 19 88.0    Cuttings
# Week 20 50.0    Cuttings
# Week 21 13.0    Cuttings
# Week 22 0.0     Cuttings
# Week 23 0.0     Cuttings


# Input:
# Enter the number of starting cuttings: 50
# Enter the week to start planting: 4

# Expected output:
# Iteration: 2
# Supply per sales week for the initial batch
# Week 1  0       Cuttings
# Week 2  0       Cuttings
# Week 3  0       Cuttings
# Week 4  0       Cuttings
# Week 5  0       Cuttings
# Week 6  0.0     Cuttings
# Week 7  50.0    Cuttings
# Week 8  100.0   Cuttings
# Week 9  150.0   Cuttings
# Week 10 200.0   Cuttings
# Week 11 250.0   Cuttings
# Week 12 250.0   Cuttings
# Week 13 250.0   Cuttings
# Week 14 250.0   Cuttings
# Week 15 250.0   Cuttings
# Week 16 175.0   Cuttings
# Week 17 100.0   Cuttings
# Week 18 25.0    Cuttings
# Week 19 0.0     Cuttings
# Week 20 0.0     Cuttings

# Iteration: 2
# Updated demand per sales week
# Week 1  0       Cuttings
# Week 2  0       Cuttings
# Week 3  0.0     Cuttings
# Week 4  0.0     Cuttings
# Week 5  0.0     Cuttings
# Week 6  0.0     Cuttings
# Week 7  0.0     Cuttings
# Week 8  0.0     Cuttings
# Week 9  0.0     Cuttings
# Week 10 25.0    Cuttings
# Week 11 50.0    Cuttings
# Week 12 75.0    Cuttings
# Week 13 100.0   Cuttings
# Week 14 125.0   Cuttings
# Week 15 125.0   Cuttings
# Week 16 125.0   Cuttings
# Week 17 125.0   Cuttings
# Week 18 125.0   Cuttings
# Week 19 88.0    Cuttings
# Week 20 50.0    Cuttings
# Week 21 13.0    Cuttings
# Week 22 0.0     Cuttings
# Week 23 0.0     Cuttings


# Input:
# Enter the number of starting cuttings: 25
# Enter the week to start planting: 7

# Expected output:
# Iteration: 3
# Supply per sales week for the initial batch
# Week 1  0       Cuttings
# Week 2  0       Cuttings
# Week 3  0       Cuttings
# Week 4  0       Cuttings
# Week 5  0       Cuttings
# Week 6  0       Cuttings
# Week 7  0       Cuttings
# Week 8  0       Cuttings
# Week 9  0.0     Cuttings
# Week 10 25.0    Cuttings
# Week 11 50.0    Cuttings
# Week 12 75.0    Cuttings
# Week 13 100.0   Cuttings
# Week 14 125.0   Cuttings
# Week 15 125.0   Cuttings
# Week 16 125.0   Cuttings
# Week 17 125.0   Cuttings
# Week 18 125.0   Cuttings
# Week 19 87.5    Cuttings
# Week 20 50.0    Cuttings
# Week 21 12.5    Cuttings
# Week 22 0.0     Cuttings
# Week 23 0.0     Cuttings


# Iteration: 3
# Updated demand per sales week
# Week 1  0       Cuttings
# Week 2  0       Cuttings
# Week 3  0.0     Cuttings
# Week 4  0.0     Cuttings
# Week 5  0.0     Cuttings
# Week 6  0.0     Cuttings
# Week 7  0.0     Cuttings
# Week 8  0.0     Cuttings
# Week 9  0.0     Cuttings
# Week 10 0.0     Cuttings
# Week 11 0.0     Cuttings
# Week 12 0.0     Cuttings
# Week 13 0.0     Cuttings
# Week 14 0.0     Cuttings
# Week 15 0.0     Cuttings
# Week 16 0.0     Cuttings
# Week 17 0.0     Cuttings
# Week 18 0.0     Cuttings
# Week 19 0.5     Cuttings
# Week 20 0.0     Cuttings
# Week 21 0.5     Cuttings
# Week 22 0.0     Cuttings
# Week 23 0.0     Cuttings
# Week 24 0.0     Cuttings
# Week 25 0.0     Cuttings
# Week 26 0.0     Cuttings
# Week 27 0.0     Cuttings
# Week 28 0.0     Cuttings
# Week 29 0.0     Cuttings
# Week 30 0.0     Cuttings
# Week 31 0.0     Cuttings
# Week 32 0       Cuttings