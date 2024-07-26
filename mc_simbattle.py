import numpy as np
import matplotlib.pyplot as plt

def simulate_battle(troops_A, troops_B, effectiveness_A, effectiveness_B, terrain_advantage_A, terrain_advantage_B, iterations):
    """
    Simulate a battlefield scenario using Monte Carlo simulation.
    
    Parameters:
    troops_A : int : initial number of troops for Force A
    troops_B : int : initial number of troops for Force B
    effectiveness_A : float : weapon effectiveness for Force A
    effectiveness_B : float : weapon effectiveness for Force B
    terrain_advantage_A : float : terrain advantage for Force A
    terrain_advantage_B : float : terrain advantage for Force B
    iterations : int : number of Monte Carlo simulations
    
    Returns:
    results : dict : dictionary containing the number of victories for each force and the number of draws
    """
    victories_A = 0
    victories_B = 0
    draws = 0
    
    for _ in range(iterations):
        remaining_troops_A = troops_A
        remaining_troops_B = troops_B
        
        while remaining_troops_A > 0 and remaining_troops_B > 0:
            casualties_A = np.random.binomial(remaining_troops_A, effectiveness_B * terrain_advantage_B)
            casualties_B = np.random.binomial(remaining_troops_B, effectiveness_A * terrain_advantage_A)
            
            remaining_troops_A -= casualties_A
            remaining_troops_B -= casualties_B
        
        if remaining_troops_A > 0:
            victories_A += 1
        elif remaining_troops_B > 0:
            victories_B += 1
        else:
            draws += 1
    
    results = {
        'victories_A': victories_A,
        'victories_B': victories_B,
        'draws': draws
    }
    
    return results

def plot_battle_results(results, iterations):
    """
    Plot the results of the battlefield simulation.
    
    Parameters:
    results : dict : dictionary containing the number of victories for each force and the number of draws
    iterations : int : number of Monte Carlo simulations
    """
    labels = ['Force A Wins', 'Force B Wins', 'Draws']
    counts = [results['victories_A'], results['victories_B'], results['draws']]
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color=['blue', 'red', 'gray'])
    plt.xlabel('Outcome')
    plt.ylabel('Frequency')
    plt.title('Monte Carlo Simulation of Battlefield Outcomes')
    plt.show()

# Parameters
troops_A = 700000  # Initial number of troops for Force A
troops_B = 350000  # Initial number of troops for Force B
effectiveness_A = 0.06  # Weapon effectiveness for Force A
effectiveness_B = 0.05  # Weapon effectiveness for Force B
terrain_advantage_A = 1.0  # Terrain advantage for Force A
terrain_advantage_B = 1.1  # Terrain advantage for Force B
iterations = 10000  # Number of Monte Carlo simulations

# Run the Monte Carlo simulation
results = simulate_battle(troops_A, troops_B, effectiveness_A, effectiveness_B, terrain_advantage_A, terrain_advantage_B, iterations)

# Print the results
print(f"Force A Wins: {results['victories_A']} ({results['victories_A'] / iterations:.2%})")
print(f"Force B Wins: {results['victories_B']} ({results['victories_B'] / iterations:.2%})")
print(f"Draws: {results['draws']} ({results['draws'] / iterations:.2%})")

# Plot the simulation results
plot_battle_results(results, iterations)
