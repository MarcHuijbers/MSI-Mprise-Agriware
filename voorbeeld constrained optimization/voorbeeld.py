import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Definieer de vraagfunctie met variatie per week
def demand_function(p, delta):
    return 50 - p + delta

# Definieer de aanbodfunctie
def supply_function(p, c):
    return p - c

# Doelstelling om het verschil tussen vraag en aanbod minimaal 1 te maken
def objective_function(x, delta):
    p, c = x
    q_d = demand_function(p, delta)
    q_s = supply_function(p, c)
    return abs(q_s - q_d - 1)

# Beperkingen
def constraint1(x):
    return x[0]  # p >= 0

def constraint2(x):
    return x[1]  # c >= 0

def constraint3(x, delta):
    p, c = x
    return supply_function(p, c) - demand_function(p, delta) - 1  # q_s >= q_d + 1

# Bereken en plot voor meerdere weken
weeks = range(1, 6)
deltas = np.random.randint(-10, 10, size=len(weeks))  # Random variatie in vraag per week

for i, delta in zip(weeks, deltas):
    # Initialiseer beperkingen
    constraints = [
        {'type': 'ineq', 'fun': constraint1},
        {'type': 'ineq', 'fun': constraint2},
        {'type': 'ineq', 'fun': lambda x: constraint3(x, delta)}
    ]

    # Definieer een startpunt
    x0 = np.array([10, 5])

    # Voer de optimalisatie uit
    result = minimize(objective_function, x0, args=(delta,), constraints=constraints, method='SLSQP')

    # Resultaten weergeven
    if result.success:
        p_opt, c_opt = result.x
        q_d_opt = demand_function(p_opt, delta)
        q_s_opt = supply_function(p_opt, c_opt)
        print(f'Week {i}:')
        print(f'  Optimale prijs (p): {p_opt}')
        print(f'  Optimale productiekosten (c): {c_opt}')
        print(f'  Optimale vraag (q_d): {q_d_opt}')
        print(f'  Optimale aanbod (q_s): {q_s_opt}')

        # Genereren van de grafiek
        p_values = np.linspace(0, 50, 400)
        q_d_values = demand_function(p_values, delta)
        q_s_values = [supply_function(p, c_opt) for p in p_values]

        plt.figure(figsize=(10, 6))
        plt.plot(p_values, q_d_values, label=f'Vraag (Week {i}, delta={delta})')
        plt.plot(p_values, q_s_values, label=f'Aanbod (c={c_opt:.2f})')
        plt.scatter([p_opt], [q_d_opt], color='red', zorder=5, label='Optimale Vraag')
        plt.scatter([p_opt], [q_s_opt], color='blue', zorder=5, label='Optimale Aanbod')
        plt.axvline(x=p_opt, color='gray', linestyle='--')
        plt.axhline(y=q_d_opt, color='gray', linestyle='--')
        plt.xlabel('Prijs (p)')
        plt.ylabel('Hoeveelheid (q)')
        plt.title(f'Vraag en Aanbod Curves voor Week {i}')
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print(f'Week {i}: Optimalisatie is niet geslaagd: {result.message}')
