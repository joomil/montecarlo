import numpy as np
import matplotlib.pyplot as plt

def get_random_returns(years, mean_return=0.07, std_dev=0.15):
    """
    Generate random annual returns based on a normal distribution.
    """
    return np.random.normal(mean_return, std_dev, years)

def simulate_portfolio_growth(starting_pot, annual_contributions, years, mean_return, std_dev, iterations):
    """
    Simulate the growth of an investment portfolio over time.
    """
    results = []
    for _ in range(iterations):
        pot = starting_pot
        yearly_values = [pot]
        returns = get_random_returns(years, mean_return, std_dev)
        for annual_return in returns:
            pot *= (1 + annual_return)
            pot += annual_contributions
            yearly_values.append(pot)
        results.append(yearly_values)
    return np.array(results)

def plot_simulation(results, years):
    """
    Plot the results of the Monte Carlo simulation.
    """
    plt.figure(figsize=(10, 6))
    for result in results:
        plt.plot(result, color='blue', alpha=0.1)
    plt.xlabel('Years')
    plt.ylabel('Portfolio Value')
    plt.title('Monte Carlo Simulation of Investment Portfolio Growth')
    plt.show()

def plot_distribution(final_values):
    """
    Plot the distribution of final portfolio values.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(final_values, bins=50, edgecolor='black')
    plt.xlabel('Final Portfolio Value')
    plt.ylabel('Frequency')
    plt.title('Distribution of Final Portfolio Values')
    plt.show()

# Parameters
starting_pot = 10000  # Initial investment amount
annual_contributions = 5000  # Annual contributions
years = 30  # Number of years
mean_return = 0.07  # Mean annual return
std_dev = 0.15  # Standard deviation of annual returns
iterations = 10000  # Number of Monte Carlo simulations

# Run the Monte Carlo simulation
results = simulate_portfolio_growth(starting_pot, annual_contributions, years, mean_return, std_dev, iterations)

# Analyze the results
final_values = results[:, -1]
mean_final_value = np.mean(final_values)
median_final_value = np.median(final_values)
lower_confidence = np.percentile(final_values, 5)
upper_confidence = np.percentile(final_values, 95)

# Print the results
print(f"Mean final portfolio value: ${mean_final_value:,.2f}")
print(f"Median final portfolio value: ${median_final_value:,.2f}")
print(f"5% confidence interval: ${lower_confidence:,.2f} - ${upper_confidence:,.2f}")

# Plot the simulation results
plot_simulation(results, years)

# Plot the distribution of final portfolio values
plot_distribution(final_values)
