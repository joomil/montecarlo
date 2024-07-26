import numpy as np
import matplotlib.pyplot as plt

def simulate_task_completion_times(num_tasks, mean_time, std_dev_time):
    """
    Simulate random task completion times based on a normal distribution.
    
    Parameters:
    num_tasks : int : number of tasks
    mean_time : float : mean task completion time
    std_dev_time : float : standard deviation of task completion times
    
    Returns:
    task_times : ndarray : simulated task completion times
    """
    return np.random.normal(mean_time, std_dev_time, num_tasks)

def calculate_project_completion_time(task_times):
    """
    Calculate the total project completion time.
    
    Parameters:
    task_times : ndarray : task completion times
    
    Returns:
    total_time : float : total project completion time
    """
    return np.sum(task_times)

def monte_carlo_project_simulation(num_tasks, mean_time, std_dev_time, deadline, iterations):
    """
    Perform a Monte Carlo simulation to estimate the probability of meeting the project deadline.
    
    Parameters:
    num_tasks : int : number of tasks
    mean_time : float : mean task completion time
    std_dev_time : float : standard deviation of task completion times
    deadline : float : project deadline
    iterations : int : number of Monte Carlo simulations
    
    Returns:
    completion_times : ndarray : simulated project completion times
    """
    completion_times = np.zeros(iterations)
    for i in range(iterations):
        task_times = simulate_task_completion_times(num_tasks, mean_time, std_dev_time)
        completion_times[i] = calculate_project_completion_time(task_times)
    return completion_times

def plot_completion_time_distribution(completion_times, deadline):
    """
    Plot the distribution of project completion times.
    
    Parameters:
    completion_times : ndarray : simulated project completion times
    deadline : float : project deadline
    """
    plt.figure(figsize=(10, 6))
    plt.hist(completion_times, bins=50, edgecolor='black')
    plt.axvline(deadline, color='red', linestyle='dashed', linewidth=2, label='Deadline')
    plt.xlabel('Project Completion Time')
    plt.ylabel('Frequency')
    plt.title('Distribution of Project Completion Times')
    plt.legend()
    plt.show()

# Parameters
num_tasks = 10  # Number of tasks
mean_time = 5  # Mean task completion time (days)
std_dev_time = 2  # Standard deviation of task completion times (days)
deadline = 50  # Project deadline (days)
iterations = 10000  # Number of Monte Carlo simulations

# Run the Monte Carlo simulation
completion_times = monte_carlo_project_simulation(num_tasks, mean_time, std_dev_time, deadline, iterations)

# Analyze the results
mean_completion_time = np.mean(completion_times)
median_completion_time = np.median(completion_times)
probability_meeting_deadline = np.sum(completion_times <= deadline) / iterations

# Print the results
print(f"Mean project completion time: {mean_completion_time:.2f} days")
print(f"Median project completion time: {median_completion_time:.2f} days")
print(f"Probability of meeting the deadline: {probability_meeting_deadline:.2%}")

# Plot the distribution of project completion times
plot_completion_time_distribution(completion_times, deadline)
