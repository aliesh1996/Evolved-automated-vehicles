import pygame
import random
import sys

# Pygame initialization
pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Random Driving Cars and Obstacles")

# Colors and settings
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
car_size = (50, 30)
obstacle_size = (50, 50)
num_obstacles = 5
num_cars = 10
fps = 60

# Clock for framerate control
clock = pygame.time.Clock()

def create_obstacles(num):
    return [[random.randint(0, screen_width - obstacle_size[0]), random.randint(0, screen_height - obstacle_size[1])] for _ in range(num)]

class Car:
    def __init__(self):
        self.x = random.randint(0, screen_width - car_size[0])
        self.y = random.randint(0, screen_height - car_size[1])
        self.speed = random.uniform(1, 3)  # Slower speed for more control
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def draw(self):
        pygame.draw.rect(screen, red, [self.x, self.y, car_size[0], car_size[1]])

    def move(self):
        # Change direction randomly
        if random.randint(1, 20) == 1:  # Occasionally change direction
            self.direction = random.choice(['left', 'right', 'up', 'down'])

        if self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed
        elif self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed
        
        # Keep within screen bounds
        self.x = max(0, min(self.x, screen_width - car_size[0]))
        self.y = max(0, min(self.y, screen_height - car_size[1]))

def game_loop():
    obstacles = create_obstacles(num_obstacles)
    cars = [Car() for _ in range(num_cars)]  # Initialize cars

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(black)

        # Draw obstacles
        for obs in obstacles:
            pygame.draw.rect(screen, green, [obs[0], obs[1], obstacle_size[0], obstacle_size[1]])

        # Update and draw cars
        for car in cars:
            car.move()
            car.draw()

        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__':
    game_loop()



