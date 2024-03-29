import numpy as np
import random
import matplotlib.pyplot as plt

# Environment setup
grid_size = (10, 10)
start = (0, 0)
goal = (9, 9)
obstacles = [(3, 3), (3, 4), (4, 4), (4, 3), (5, 5), (6, 5), (5, 6)]
population_size = 500
mutation_rate = 0.01
generations = 1000

# Initialize grid: 0 - free, -1 - start, -2 - goal, 1 - obstacle
grid = np.zeros(grid_size)
for obs in obstacles:
    grid[obs] = 1

def initialize_population(size):
    """Initialize a population of random paths."""
    population = []
    for _ in range(size):
        path_length = np.random.randint(low=20, high=40) # Random path length
        path = [np.random.choice(['up', 'down', 'left', 'right']) for _ in range(path_length)]
        population.append(path)
    return population

def evaluate_path(path):
    """Evaluate a path based on its ability to reach the goal and avoid obstacles."""
    x, y = start
    for move in path:
        if move == 'up' and y < grid_size[1] - 1: y += 1
        elif move == 'down' and y > 0: y -= 1
        elif move == 'left' and x > 0: x -= 1
        elif move == 'right' and x < grid_size[0] - 1: x += 1
        if grid[y, x] == 1: return -1 # Path hits an obstacle
    if (y, x) == goal:
        return 100 - len(path) # Reward for reaching the goal, shorter paths are better
    return -1 # Did not reach the goal

def select_parents(population, scores, num_parents):
    """Select the top-scoring paths to be parents for the next generation."""
    parents_indices = np.argsort(scores)[-num_parents:]
    return [population[i] for i in parents_indices]

def crossover(parent1, parent2):
    """Combine two paths to produce a new path."""
    crossover_point = np.random.randint(1, min(len(parent1), len(parent2)))
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(path):
    """Randomly mutate a path."""
    for i in range(len(path)):
        if np.random.rand() < mutation_rate:
            path[i] = np.random.choice(['up', 'down', 'left', 'right'])
    return path

def plot_path(grid, path):
    """Plot the path on the grid."""
    plt.figure(figsize=(5, 5))
    ax = plt.gca()
    ax.set_xlim([0, grid.shape[1]])
    ax.set_ylim([0, grid.shape[0]])
    plt.imshow(grid, cmap='Greys', origin='lower')
    
    # Draw the start and goal
    plt.scatter(start[1], start[0], marker='o', color='green', s=100, label='Start')
    plt.scatter(goal[1], goal[0], marker='o', color='red', s=100, label='Goal')
    
    # Draw the path
    y, x = start
    for move in path:
        if move == 'up' and y < grid_size[1] - 1: y += 1
        elif move == 'down' and y > 0: y -= 1
        elif move == 'left' and x > 0: x -= 1
        elif move == 'right' and x < grid_size[0] - 1: x += 1
        plt.scatter(x, y, marker='.', color='blue')
    
    plt.grid(True)
    plt.legend()
    plt.show()

def evolutionary_algorithm():
    population = initialize_population(population_size)
    for generation in range(generations):
        scores = [evaluate_path(path) for path in population]
        print(f"Generation {generation}: Best score = {max(scores)}")
        if max(scores) > 0: # Success condition
            best_index = np.argmax(scores)
            best_path = population[best_index]
            print("Found a path to the goal!")
            vis_grid = np.copy(grid)
            vis_grid[start] = -1  # Mark start
            vis_grid[goal] = -2   # Mark goal
            plot_path(vis_grid, best_path)
            return best_path
        parents = select_parents(population, scores, population_size // 2)
        next_population = []
        while len(next_population) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_population.append(child)
        population = next_population
    return None

best_path = evolutionary_algorithm()
if best_path:
    print("Best path found:", best_path)
else:
    print("Failed to find a path to the goal.")


