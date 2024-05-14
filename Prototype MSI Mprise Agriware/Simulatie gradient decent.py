import numpy as np
import matplotlib.pyplot as plt

# Functie om totale aanbod te berekenen voor een gegeven aantal planten per week en productiecurves van alle planten
def total_supply(start_weeks, start_plants, production_curve, num_weeks):
    # Bepaal het totale aanbod voor elke startweek en aantal beginplanten
    total = np.zeros(num_weeks)
    for start_week, start_plant in zip(start_weeks, start_plants):
        plants_per_week = np.zeros(num_weeks)
        for i in range(num_weeks):
            if i >= start_week:
                index = i - start_week
                if index >= 0:
                    plants_per_week[i] = start_plant * production_curve[int(index)]  # Zorg ervoor dat index een geheel getal is
        total += np.cumsum(plants_per_week)
    return total

# Functie om dynamische productiecurve te genereren
def generate_production_curve():
    # Productie schema in procenten
    production_scheme = np.array([20, 40, 60, 80, 100, 100, 100, 100, 100, 70, 40, 10])
    # Converteer percentages naar decimale vorm
    production_scheme = production_scheme / 100.0
    # Lineaire interpolatie tussen de weken
    production_curve = np.interp(np.arange(12), np.arange(len(production_scheme)), production_scheme)
    return production_curve

# Functie om totale vraag te berekenen voor een gegeven week
def total_demand(week):
    # Implementeer hier de logica om de totale vraag voor een gegeven week te berekenen
    pass

# Aangepaste loss functie met productiecurves en vraagcurve
def custom_loss(start_weeks, start_plants, production_curve, demand_curve):
    total = total_supply(start_weeks, start_plants, production_curve, len(demand_curve))
    loss = np.sum((total - demand_curve)**2)
    return loss

# Gradient descent voor het optimaliseren van het aantal planten per startweek
def gradient_descent(production_curve, demand_curve, learning_rate=0.01, num_iterations=1000):
    num_weeks = len(demand_curve)  # Aantal weken
    
    # Willekeurige initiële parameters (startweken en aantal beginplanten)
    start_weeks = np.random.randint(0, num_weeks, size=10).astype(np.float64)  # 10 willekeurige startweken
    start_plants = np.random.randint(1, 20, size=10).astype(np.float64)  # 10 willekeurige aantal beginplanten
    
    losses = []  # Om de loss functie tijdens de iteraties op te slaan
    
    for _ in range(num_iterations):
        # Bereken de loss functie
        loss = custom_loss(start_weeks, start_plants, production_curve, demand_curve)
        losses.append(loss)
        
        # Bereken de gradient van de loss functie met betrekking tot de startweken en aantal beginplanten
        gradient_weeks = np.zeros_like(start_weeks)
        gradient_plants = np.zeros_like(start_plants)
        for i in range(len(start_weeks)):
            start_weeks_copy = start_weeks.copy()
            start_weeks_copy[i] += 1  # Een kleine verandering toepassen op de startweek
            loss_plus = custom_loss(start_weeks_copy, start_plants, production_curve, demand_curve)
            start_weeks_copy[i] -= 2  # Terug naar de oorspronkelijke waarde en nog een kleine verandering toepassen
            loss_minus = custom_loss(start_weeks_copy, start_plants, production_curve, demand_curve)
            gradient_weeks[i] = (loss_plus - loss_minus) / 2
            
            start_plants_copy = start_plants.copy()
            start_plants_copy[i] += 1  # Een kleine verandering toepassen op het aantal beginplanten
            loss_plus = custom_loss(start_weeks, start_plants_copy, production_curve, demand_curve)
            start_plants_copy[i] -= 2  # Terug naar de oorspronkelijke waarde en nog een kleine verandering toepassen
            loss_minus = custom_loss(start_weeks, start_plants_copy, production_curve, demand_curve)
            gradient_plants[i] = (loss_plus - loss_minus) / 2
        
        # Update de parameters (startweken en aantal beginplanten) met de gradient descent update regel
        start_weeks -= learning_rate * gradient_weeks
        start_plants -= learning_rate * gradient_plants
    
    return start_weeks, start_plants, losses

# Voorbeeld van productiecurves voor twee planten over 10 weken
production_curve = generate_production_curve()

# Voorbeeld van een vraagcurve voor 10 weken
demand_curve = np.random.rand(10) * 100  # Willekeurige vraagcurve

# Voer gradient descent uit om het optimale aantal planten per startweek te vinden
best_start_weeks, best_start_plants, best_loss = gradient_descent(production_curve, demand_curve)

# Bereken het totale aanbod voor elke week op basis van het optimale aantal planten per startweek
total_supply = total_supply(best_start_weeks.astype(int), best_start_plants.astype(int), production_curve, len(demand_curve))

# Print het totale aanbod per week
for week, supply in enumerate(total_supply, start=1):
    print(f"Week {week}: {supply}")
# Plot van de vraag- en totale aanbodlijnen
weeks = np.arange(1, len(demand_curve) + 1)
plt.plot(weeks, demand_curve, label='Vraaglijn')
plt.plot(weeks, total_supply, label='Totale Aanbodlijn')
plt.xlabel('Week')
plt.ylabel('Aantal')
plt.title('Vraag- en Totale Aanbodlijnen')
plt.legend()
plt.show()

# Plot van de productiecurve
weeks = np.arange(1, len(production_curve) + 1)
plt.plot(weeks, production_curve, marker='o')
plt.xlabel('Week')
plt.ylabel('Productie Percentage')
plt.title('Dynamische Productiecurve')
plt.grid(True)
plt.show()
