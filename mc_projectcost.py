import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the activity cost ranges
activity_costs = {
    'A': (10000, 20000),
    'B': (15000, 15000),
    'C': (7500, 12000),
    'D': (4800, 6200),
    'E': (20000, 25000),
    'F': (5000, 7000)
}

def generate_random_costs(activity_costs):
    """
    Generate random costs for each activity based on a uniform distribution.
    
    Parameters:
    activity_costs : dict : dictionary with activity names as keys and (min, max) cost tuples as values
    
    Returns:
    costs : dict : dictionary with activity names as keys and random costs as values
    """
    costs = {}
    for activity, (min_cost, max_cost) in activity_costs.items():
        costs[activity] = np.random.uniform(min_cost, max_cost)
    return costs

def calculate_total_cost(costs):
    """
    Calculate the total project cost by summing the activity costs.
    
    Parameters:
    costs : dict : dictionary with activity names as keys and costs as values
    
    Returns:
    total_cost : float : total project cost
    """
    return sum(costs.values())

def monte_carlo_project_cost_simulation(activity_costs, iterations):
    """
    Perform a Monte Carlo simulation to estimate the total project cost.
    
    Parameters:
    activity_costs : dict : dictionary with activity names as keys and (min, max) cost tuples as values
    iterations : int : number of Monte Carlo simulations
    
    Returns:
    total_costs : ndarray : simulated total project costs
    """
    total_costs = np.zeros(iterations)
    for i in range(iterations):
        costs = generate_random_costs(activity_costs)
        total_costs[i] = calculate_total_cost(costs)
    return total_costs

def plot_cost_distribution(total_costs):
    """
    Plot the distribution of total project costs.
    
    Parameters:
    total_costs : ndarray : simulated total project costs
    """
    plt.figure(figsize=(10, 6))
    plt.hist(total_costs, bins=50, edgecolor='black')
    plt.xlabel('Total Project Cost')
    plt.ylabel('Frequency')
    plt.title('Distribution of Total Project Costs from Monte Carlo Simulation')
    plt.show()

# Parameters
iterations = 10000  # Number of Monte Carlo simulations

# Run the Monte Carlo simulation
total_costs = monte_carlo_project_cost_simulation(activity_costs, iterations)

# Analyze the results
mean_cost = np.mean(total_costs)
median_cost = np.median(total_costs)
probability_exceeding_100k = np.sum(total_costs > 100000) / iterations

# Print the results
print(f"Mean total project cost: ${mean_cost:,.2f}")
print(f"Median total project cost: ${median_cost:,.2f}")
print(f"Probability of exceeding $100,000: {probability_exceeding_100k:.2%}")

# Plot the distribution of total project costs
plot_cost_distribution(total_costs)
