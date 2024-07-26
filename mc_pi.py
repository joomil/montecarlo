import random
import matplotlib.pyplot as plt

def monte_carlo_pi(num_points):
    inside_circle = 0
    points_x = []
    points_y = []
    colors = []

    for _ in range(num_points):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        distance = x**2 + y**2

        points_x.append(x)
        points_y.append(y)
        if distance <= 1:
            inside_circle += 1
            colors.append('blue')
        else:
            colors.append('red')

    pi_estimate = (inside_circle / num_points) * 4
    return pi_estimate, points_x, points_y, colors

def plot_simulation(points_x, points_y, colors):
    plt.figure(figsize=(6, 6))
    plt.scatter(points_x, points_y, c=colors, s=1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Monte Carlo Simulation for Estimating π')
    plt.show()

# Number of random points to generate
num_points = 10000

# Run the Monte Carlo simulation
pi_estimate, points_x, points_y, colors = monte_carlo_pi(num_points)

# Print the estimated value of π
print(f"Estimated value of pi after {num_points} points: {pi_estimate}")

# Plot the simulation
plot_simulation(points_x, points_y, colors)
