import numpy as np
import matplotlib.pyplot as plt

# Functie om totale aanbod te berekenen voor een gegeven aantal planten per week en productiecurves van alle planten
def total_supply(plants_per_week, production_curves):
    total = np.sum([plants * curve for plants, curve in zip(plants_per_week, production_curves)])
    return total

# Functie om totale vraag te berekenen voor een gegeven week
def total_demand(week):
    # Implementeer hier de logica om de totale vraag voor een gegeven week te berekenen
    pass

# Functie om brute-force search uit te voeren om het optimale aantal planten per week te vinden
def brute_force_search(production_curves):
    num_weeks = len(production_curves[0])  # Aantal weken

    best_plants_per_week = None
    best_total_supply = float('-inf')

    for plants1 in range(1, 11):  # Mogelijke aantal planten per week voor plant 1
        for plants2 in range(1, 11):  # Mogelijke aantal planten per week voor plant 2
            # Bereken totale aanbod voor deze combinatie van planten per week
            total_supply_this_week = total_supply([plants1, plants2], production_curves)

            # Controleer of dit het beste aanbod tot nu toe is
            if total_supply_this_week > best_total_supply:
                best_plants_per_week = [plants1, plants2]
                best_total_supply = total_supply_this_week

    return best_plants_per_week, best_total_supply

# Voorbeeld van productiecurves voor twee planten over 10 weken
production_curves = [
    [np.random.rand() * 10 for _ in range(10)],  # Productiecurve voor plant 1
    [np.random.rand() * 10 for _ in range(10)]   # Productiecurve voor plant 2
]



# Voer brute-force search uit om het optimale aantal planten per week te vinden
best_plants_per_week, best_total_supply = brute_force_search(production_curves)

print("Optimaal aantal planten per week:", best_plants_per_week)
print("Totale aanbod:", best_total_supply)
