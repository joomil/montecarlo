import numpy as np
import matplotlib.pyplot as plt

def simulate_cash_flows(years, mean_cash_flow, std_dev_cash_flow):
    """
    Simulate random annual cash flows based on a normal distribution.
    
    Parameters:
    years : int : number of years
    mean_cash_flow : float : mean annual cash flow
    std_dev_cash_flow : float : standard deviation of annual cash flows
    
    Returns:
    cash_flows : ndarray : simulated annual cash flows
    """
    return np.random.normal(mean_cash_flow, std_dev_cash_flow, years)

def calculate_npv(initial_investment, discount_rate, cash_flows):
    """
    Calculate the Net Present Value (NPV) of a project.
    
    Parameters:
    initial_investment : float : initial investment
    discount_rate : float : discount rate
    cash_flows : ndarray : annual cash flows
    
    Returns:
    npv : float : Net Present Value
    """
    years = len(cash_flows)
    discounted_cash_flows = cash_flows / (1 + discount_rate) ** np.arange(1, years + 1)
    npv = np.sum(discounted_cash_flows) - initial_investment
    return npv

def monte_carlo_npv_simulation(initial_investment, discount_rate, years, mean_cash_flow, std_dev_cash_flow, iterations):
    """
    Perform a Monte Carlo simulation to estimate the NPV of a project.
    
    Parameters:
    initial_investment : float : initial investment
    discount_rate : float : discount rate
    years : int : number of years
    mean_cash_flow : float : mean annual cash flow
    std_dev_cash_flow : float : standard deviation of annual cash flows
    iterations : int : number of Monte Carlo simulations
    
    Returns:
    npvs : ndarray : simulated NPVs
    """
    npvs = np.zeros(iterations)
    for i in range(iterations):
        cash_flows = simulate_cash_flows(years, mean_cash_flow, std_dev_cash_flow)
        npvs[i] = calculate_npv(initial_investment, discount_rate, cash_flows)
    return npvs

def plot_npv_distribution(npvs):
    """
    Plot the distribution of NPVs.
    
    Parameters:
    npvs : ndarray : simulated NPVs
    """
    plt.figure(figsize=(10, 6))
    plt.hist(npvs, bins=50, edgecolor='black')
    plt.xlabel('NPV')
    plt.ylabel('Frequency')
    plt.title('Distribution of NPVs from Monte Carlo Simulation')
    plt.show()

# Parameters
initial_investment = 100000  # Initial investment amount
discount_rate = 0.1  # Discount rate
years = 10  # Number of years
mean_cash_flow = 20000  # Mean annual cash flow
std_dev_cash_flow = 5000  # Standard deviation of annual cash flows
iterations = 10000  # Number of Monte Carlo simulations

# Run the Monte Carlo simulation
npvs = monte_carlo_npv_simulation(initial_investment, discount_rate, years, mean_cash_flow, std_dev_cash_flow, iterations)

# Analyze the results
mean_npv = np.mean(npvs)
median_npv = np.median(npvs)
positive_npv_probability = np.sum(npvs > 0) / iterations

# Print the results
print(f"Mean NPV: ${mean_npv:,.2f}")
print(f"Median NPV: ${median_npv:,.2f}")
print(f"Probability of positive NPV: {positive_npv_probability:.2%}")

# Plot the distribution of NPVs
plot_npv_distribution(npvs)
