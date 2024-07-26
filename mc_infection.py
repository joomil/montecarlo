import numpy as np
import matplotlib.pyplot as plt

def simulate_disease_spread(population_size, initial_infected, transmission_rate, recovery_rate, days, iterations):
    """
    Simulate the spread of a disease within a population using Monte Carlo simulation.
    
    Parameters:
    population_size : int : total population size
    initial_infected : int : initial number of infected individuals
    transmission_rate : float : probability of disease transmission per contact
    recovery_rate : float : probability of recovery per day
    days : int : number of days to simulate
    iterations : int : number of Monte Carlo simulations
    
    Returns:
    infection_counts : ndarray : simulated number of infected individuals over time
    """
    infection_counts = np.zeros((days, iterations))
    
    for i in range(iterations):
        infected = initial_infected
        recovered = 0
        susceptible = population_size - infected
        
        daily_infections = []
        
        for day in range(days):
            new_infections = np.random.binomial(susceptible, transmission_rate * infected / population_size)
            new_recoveries = np.random.binomial(infected, recovery_rate)
            
            infected += new_infections - new_recoveries
            susceptible -= new_infections
            recovered += new_recoveries
            
            daily_infections.append(infected)
        
        infection_counts[:, i] = daily_infections
    
    return infection_counts

def plot_disease_spread(infection_counts):
    """
    Plot the number of infected individuals over time.
    
    Parameters:
    infection_counts : ndarray : simulated number of infected individuals over time
    """
    mean_infections = np.mean(infection_counts, axis=1)
    lower_confidence = np.percentile(infection_counts, 5, axis=1)
    upper_confidence = np.percentile(infection_counts, 95, axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(mean_infections, label='Mean Infections')
    plt.fill_between(range(len(mean_infections)), lower_confidence, upper_confidence, color='gray', alpha=0.5, label='90% Confidence Interval')
    plt.xlabel('Days')
    plt.ylabel('Number of Infected Individuals')
    plt.title('Monte Carlo Simulation of Disease Spread')
    plt.legend()
    plt.show()

def plot_final_infection_distribution(infection_counts):
    """
    Plot the distribution of final infection counts.
    
    Parameters:
    infection_counts : ndarray : simulated number of infected individuals over time
    """
    final_infections = infection_counts[-1]
    
    plt.figure(figsize=(10, 6))
    plt.hist(final_infections, bins=50, edgecolor='black')
    plt.xlabel('Final Number of Infected Individuals')
    plt.ylabel('Frequency')
    plt.title('Distribution of Final Infection Counts from Monte Carlo Simulation')
    plt.show()

# Parameters
population_size = 8000000000  # Total population size
initial_infected = 1  # Initial number of infected individuals
transmission_rate = 1  # Probability of disease transmission per contact
recovery_rate = 0.05  # Probability of recovery per day
days = 365  # Number of days to simulate
iterations = 1000  # Number of Monte Carlo simulations

# Run the Monte Carlo simulation
infection_counts = simulate_disease_spread(population_size, initial_infected, transmission_rate, recovery_rate, days, iterations)

# Plot the simulation results
plot_disease_spread(infection_counts)

# Plot the distribution of final infection counts
plot_final_infection_distribution(infection_counts)
