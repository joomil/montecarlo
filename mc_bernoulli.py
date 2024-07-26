import numpy as np
import matplotlib.pyplot as plt

def simulate_bernoulli_trials(num_trials, prob_success):
    """
    Simulate a series of Bernoulli trials.
    
    Parameters:
    num_trials : int : number of trials
    prob_success : float : probability of success for each trial
    
    Returns:
    successes : int : number of successes
    """
    trials = np.random.binomial(1, prob_success, num_trials)
    successes = np.sum(trials)
    return successes

def monte_carlo_bernoulli_simulation(num_trials, prob_success, target_successes, iterations):
    """
    Perform a Monte Carlo simulation to estimate the probability of achieving a certain number of successes.
    
    Parameters:
    num_trials : int : number of trials
    prob_success : float : probability of success for each trial
    target_successes : int : target number of successes
    iterations : int : number of Monte Carlo simulations
    
    Returns:
    success_counts : ndarray : simulated number of successes
    """
    success_counts = np.zeros(iterations)
    for i in range(iterations):
        success_counts[i] = simulate_bernoulli_trials(num_trials, prob_success)
    return success_counts

def plot_success_distribution(success_counts, target_successes):
    """
    Plot the distribution of the number of successes.
    
    Parameters:
    success_counts : ndarray : simulated number of successes
    target_successes : int : target number of successes
    """
    plt.figure(figsize=(10, 6))
    plt.hist(success_counts, bins=range(int(success_counts.min()), int(success_counts.max()) + 2), edgecolor='black', align='left')
    plt.axvline(target_successes, color='red', linestyle='dashed', linewidth=2, label=f'Target: {target_successes}')
    plt.xlabel('Number of Successes')
    plt.ylabel('Frequency')
    plt.title('Distribution of Number of Successes from Monte Carlo Simulation')
    plt.legend()
    plt.show()

# Parameters
num_trials = 100  # Number of trials
prob_success = 0.5  # Probability of success for each trial
target_successes = 60  # Target number of successes
iterations = 10000  # Number of Monte Carlo simulations

# Run the Monte Carlo simulation
success_counts = monte_carlo_bernoulli_simulation(num_trials, prob_success, target_successes, iterations)

# Analyze the results
mean_successes = np.mean(success_counts)
median_successes = np.median(success_counts)
probability_target_successes = np.sum(success_counts >= target_successes) / iterations

# Print the results
print(f"Mean number of successes: {mean_successes:.2f}")
print(f"Median number of successes: {median_successes:.2f}")
print(f"Probability of achieving at least {target_successes} successes: {probability_target_successes:.2%}")

# Plot the distribution of the number of successes
plot_success_distribution(success_counts, target_successes)
