import numpy as np
import matplotlib.pyplot as plt
from random import randint

def throw_and_sum_n_dice(n):
    """
    This function throws n dice and sums the results.
    """
    total = 0
    for _ in range(n):
        throw = randint(1, 6)
        total += throw
    return total

def compute_profit_path(k, n):
    """
    This function returns the profit (or loss) path at the end of 
    k iterations of the game, where we throw n dice.
    """
    total_profit = 0
    for _ in range(k):
        total = throw_and_sum_n_dice(n)
        if 40 <= total <= 50:
            total_profit += 10
        else:
            total_profit -= 2
    return total_profit

# Parameters
iterations = 100000  # Number of Monte Carlo simulations
k = 50  # Number of times to play the game in each simulation
n = 10  # Number of dice thrown in each game

# Run the Monte Carlo simulation
total_profits = []
for _ in range(iterations):
    total_profits.append(compute_profit_path(k, n))

# Analyze the results
total_profits = np.array(total_profits)
winning_occurrences = np.sum(total_profits > 0)
losing_occurrences = np.sum(total_profits <= 0)

# Print the results
print(f'We would win money {winning_occurrences} times out of {iterations} simulations -- a.k.a. {winning_occurrences/iterations:.2%} of the time.')
print(f'We would lose money {losing_occurrences} times out of {iterations} simulations -- a.k.a. {losing_occurrences/iterations:.2%} of the time.')
print(f'Maximum profit: ${total_profits.max()}')
print(f'Maximum loss: ${total_profits.min()}')
print(f'Average profit/loss: ${total_profits.mean():.2f}')

# Plot the distribution of profits
plt.figure(figsize=(10, 6))
plt.hist(total_profits, bins=50, edgecolor='black')
plt.xlabel('Total Profit')
plt.ylabel('Frequency')
plt.title('Distribution of Total Profits from Monte Carlo Simulation')
plt.show()
