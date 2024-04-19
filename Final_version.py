import numpy as np
import matplotlib.pyplot as plt
from pyswarm import pso

# Grid and cell parameters
GRID_WIDTH = 10
GRID_HEIGHT = 10
CELL_SIZE = 0.125  # Adjust cell size for clarity
NUM_CELLS = 3000  # Number of cells each vehicle tries to place

def create_obstacles():
    return [
        {'type': 'circle', 'center': np.array([3, 3]), 'radius': 1},
        {'type': 'circle', 'center': np.array([6, 5]), 'radius': 1.5},
        {'type': 'rect', 'corner': np.array([1, 8]), 'size': np.array([2, 1])},
        {'type': 'rect', 'corner': np.array([8, 1]), 'size': np.array([4, 4])}
    ]

def position_intersects_obstacle(x, y, obstacles):
    for obstacle in obstacles:
        if obstacle['type'] == 'circle':
            center, radius = obstacle['center'], obstacle['radius']
            if np.linalg.norm(np.array([x, y]) - center) < radius:
                return True
        elif obstacle['type'] == 'rect':
            ox, oy, ow, oh = obstacle['corner'][0], obstacle['corner'][1], obstacle['size'][0], obstacle['size'][1]
            if x < ox + ow and x > ox and y < oy + oh and y > oy:
                return True
    return False

def run_pso_for_vehicle(cooperative=True):
    lb = [0] * (2 * NUM_CELLS)
    ub = [(GRID_WIDTH - CELL_SIZE), (GRID_HEIGHT - CELL_SIZE)] * NUM_CELLS
    fitness_history = []

    def evaluate(X):
        X = X.reshape(-1, 2)
        score = 0
        central_bias = 0.1  # Adjust bias strength
        center = np.array([GRID_WIDTH / 2, GRID_HEIGHT / 2])
        obstacles = create_obstacles()
        for x, y in X:
            if 0 <= x <= GRID_WIDTH - CELL_SIZE and 0 <= y <= GRID_HEIGHT - CELL_SIZE:
                if not position_intersects_obstacle(x, y, obstacles):
                    score += 1
                    # Stronger penalty for being far from center to encourage central placement
                    dist_to_center = np.linalg.norm(np.array([x, y]) - center)
                    score -= dist_to_center * central_bias
        fitness_history.append(-score)
        return -score

    xopt, fopt = pso(evaluate, lb, ub, swarmsize=3, omega=0.5, phip=1.5, phig=2.0, maxiter=100)
    return xopt, fitness_history

# Global best for cooperative scenario
global_best_score = float('inf')
global_best_position = None

# Run PSO for both scenarios
cooperative_solution, coop_fitness_history = run_pso_for_vehicle(cooperative=True)
non_cooperative_solution, non_coop_fitness_history = run_pso_for_vehicle(cooperative=False)

# Visualization
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
for ax in [ax1, ax2]:
    for obstacle in create_obstacles():
        if obstacle['type'] == 'circle':
            circle = plt.Circle(obstacle['center'], obstacle['radius'], color='red', alpha=0.5)
            ax.add_artist(circle)
        elif obstacle['type'] == 'rect':
            rect = plt.Rectangle(obstacle['corner'], obstacle['size'][0], obstacle['size'][1], color='blue', alpha=0.5)
            ax.add_artist(rect)

# Plotting results for cooperative scenario
positions = cooperative_solution.reshape(-1, 2)
for x, y in positions:
    if not position_intersects_obstacle(x, y, create_obstacles()):
        rect = plt.Rectangle((x, y), CELL_SIZE, CELL_SIZE, edgecolor='green', facecolor='green', alpha=0.3)
        ax1.add_artist(rect)
ax1.set_title('Cooperative Multi-Swarm PSO')
ax1.set_xlim(0, GRID_WIDTH)
ax1.set_ylim(0, GRID_HEIGHT)
ax1.set_aspect('equal')

# Plotting results for non-cooperative scenario
positions = non_cooperative_solution.reshape(-1, 2)
for x, y in positions:
    if not position_intersects_obstacle(x, y, create_obstacles()):
        rect = plt.Rectangle((x, y), CELL_SIZE, CELL_SIZE, edgecolor='purple', facecolor='purple', alpha=0.3)
        ax2.add_artist(rect)
ax2.set_title('Non-Cooperative Single Swarm PSO')
ax2.set_xlim(0, GRID_WIDTH)
ax2.set_ylim(0, GRID_HEIGHT)
ax2.set_aspect('equal')

# Plotting the fitness evolution for both scenarios
ax3.plot(coop_fitness_history, label='Cooperative', color='green')
ax3.plot(non_coop_fitness_history, label='Non-Cooperative', color='purple')
ax3.set_title('Fitness Evolution Over Generations')
ax3.set_xlabel('Generation')
ax3.set_ylabel('Fitness Score (Negative Drivable Area)')
ax3.legend()

plt.show()



