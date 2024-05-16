# Settings
MaxPiecesPerHarvest = 5
FirstHarvestWeek = 4
MinimumPlant = 5
MaximumPlant = 10

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

# stap 1: Hoeveel Planten heb ik nodig om aan het gevraagde aantal stekken te voldoen? Beginnend met de eerste week waarbij de vraag > 0 en dit wordt voldaan met de eerste harvest fase.
input = input("Voer aantal begin stekken in:")
# welke week start het planten van de stekken?


# stap 2: Wat is de output van de partij uit stap 1? Dus hoeveel stekken heb ik in welke weken?
# Calculate the output for each week
output = {}
for week in range(FirstHarvestWeek, 33):  # Loop over the weeks from the first harvest week
    # Calculate the harvest week (subtract 3 because the first harvest is 3 weeks after planting)
    harvest_week = week - 3
    input = int(input)  # Convert input to an integer
    # Get the harvest percentage for this harvest week
    percentage = productieschema.get(harvest_week, 0) / 100
    # Calculate the output for this week
    output[week] = input * percentage * MaxPiecesPerHarvest

# Print the output
print("Aanbod voor partij uit stap 1 per verkoopweek")
for week, supply in output.items():
    print(f"Week {week}\t{supply}\tStekken")
    
# stap 3: Bereken het nieuwe aantal gevraagde stekken per week? (Origineel - Output van partij, zie stap 2)
new_demand = {}
for week, demand in demand.items():
    new_demand[week] = demand - output.get(week, 0)

# Print the new demand
print("Nieuwe vraag per verkoopweek")
for week, demand in new_demand.items():
    print(f"Week {week}\t{demand}\tStekken")
    
# # stap 4: Hoeveel planten heb ik nodig om aan de nieuwe vraag te voldoen?
# # Iterate over the demand and check if the demand is greater than 0
# while any(demand > 0 for demand in new_demand.values()):
#     for week, demand in new_demand.items():
#         if demand > 0:
#             print(f"Plant {demand} stekken in week {week}")
#             # Update the new_demand by subtracting the output for this week
#             new_demand[week] -= output.get(week, 0)
        
            