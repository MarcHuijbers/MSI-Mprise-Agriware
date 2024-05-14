import numpy as np

import matplotlib.pyplot as plt

# Aangepaste loss functie, hier moeten de parameters nog aan toegevoegd worden.
def custom_loss(y_true, y_pred):
    loss = np.where(y_true > y_pred, (y_true - y_pred)**2, 0)
    return np.mean(loss)

# Gradient descent voor het trainen van het regressiemodel
def gradient_descent(X, y, learning_rate=0.01, stop_criteria=1.5):
    # Willekeurige initiële parameters voor regressiemodel
    a = np.random.randn()
    b = np.random.randn()
    prev_loss = float('inf')
    
    # Optimalisatie loop
    num_iterations = 0
    while True:
        # Voorspellingen maken met huidige parameters
        y_pred = a * X + b # hier komt de functie van de rode vraaglijn.
        
        # Berekenen van de custom loss
        loss = custom_loss(y, y_pred)
        
        # Check stopcriterium
        if abs(loss - prev_loss) < stop_criteria:
            break
        
        prev_loss = loss
        
        # Gradients berekenen
        grad_a = (-2 / len(X)) * np.sum(X * (y - y_pred))
        grad_b = (-2 / len(X)) * np.sum(y - y_pred)
        
        # Parameters bijwerken met gradient descent
        a -= learning_rate * grad_a
        b -= learning_rate * grad_b
        
        num_iterations += 1
    
    return a, b, num_iterations

# Functie om regressiemodel te trainen en custom loss te berekenen
def train_and_compute_loss(X, y, stop_criteria=1.5):
    a, b, num_iterations = gradient_descent(X, y, stop_criteria=stop_criteria)
    y_pred = a * X + b
    loss = custom_loss(y, y_pred)
    return loss, num_iterations

# Data genereren
np.random.seed(0)
X = np.random.rand(50) * 10
y = 2 * X + 1 + np.random.randn(50) * 2  # True line: y = 2X + 1

# Aantal iteraties voor de simulatie
stop_criteria = 1.5
losses = []
num_iterations = 0
while True:
    loss, iterations = train_and_compute_loss(X, y, stop_criteria=stop_criteria)
    losses.append(loss)
    num_iterations += iterations
    print("Iteratie", num_iterations, "- Custom Loss:", loss)
    if loss <= stop_criteria:
        break

# Plot van de custom loss per iteratie
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(losses)+1), losses, marker='o')
plt.xlabel('Iteratie')
plt.ylabel('Custom Loss')
plt.title('Custom Loss per Iteratie (Stopcriterium: {})'.format(stop_criteria))
plt.grid(True)
plt.show()