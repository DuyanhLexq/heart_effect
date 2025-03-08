"""
Heart Effect Description

Author: duyanhle
Last Modified: February 27, 2025

This heart effect is created using Pygame.

Heartbeat Animation: The heart expands and contracts rhythmically, with a slower expansion and a quicker contraction to mimic a natural pulse.
Glowing Gradient: The heart smoothly transitions from deep pink to a softer shade, creating a gentle glowing effect.
This effect is perfect for animations and themed events like Valentine’s Day, International Women’s Day, and more.

"""
import pygame
from typing import List
import random
import time
import math
from copy import deepcopy

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Glowing Heart")

class Pos:
    """
    Represents a position with coordinates and color.
    """
    def __init__(self, x: int, y: int, color, real_x: int, real_y: int) -> None:
        self.x = x
        self.y = y
        self.real_x = real_x
        self.real_y = real_y
        self.color = color

class Particle:
    """
    Represents a falling particle with gravity effect.
    """
    def __init__(self, x: int, y: int, color, real_x: int, real_y: int, delay: float = 0):
        self.x = x
        self.y = y
        self.real_x = real_x
        self.real_y = real_y
        self.color = color
        self.start_time = time.time() + delay  # Delay before the particle starts falling
        self.velocity = 0  # Falling velocity
        self.active = False  # Particle falls only when activated

# Constants
GRAVITY = 0.1  # Gravity force
MAX_DELAY = 2.5  # Maximum delay before falling
PARTICLE_COUNT = 1000  # Number of falling particles

#heart beat effect
speed = -0.5
v = 5
out = True


# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PINK = (219, 112, 147)
LIGHT_PINK = (255, 182, 193)
SOFTER_PINK = (255, 204, 213)

# Scale and center settings
scale = [150, 120]
center_x, center_y = WIDTH // 2, HEIGHT // 2  

def heart_equation(x, y, scale_type: int) -> bool:
    """
    Checks if a point (x, y) satisfies the heart equation.
    """
    x = x / scale[scale_type]
    y = y / scale[scale_type]
    res = (x**2 + y**2 - 1)**3 - x**2 * y**3
    return res <= 0

def get_fade_color(real_x, real_y):
    """
    Generates a color gradient effect for the heart shape.
    """
    max_distance = math.sqrt((WIDTH // 2) ** 2 + (HEIGHT // 2) ** 2)
    distance = math.sqrt(real_x**2 + real_y**2)
    fade_factor = 1 - (distance / max_distance)
    fade_factor = max(0, fade_factor)
    
    r = int(PINK[0] * fade_factor + SOFTER_PINK[0] * (1 - fade_factor))
    g = int(PINK[1] * fade_factor + SOFTER_PINK[1] * (1 - fade_factor))
    b = int(PINK[2] * fade_factor + SOFTER_PINK[2] * (1 - fade_factor))
    
    return (r, g, b)

def get_pos_begin(heart_data: List[Pos], scale_type: int):
    """
    Generates initial heart shape positions.
    """
    for real_x in range(-WIDTH // 2, WIDTH // 2, 1):  
        for real_y in range(-HEIGHT // 2, HEIGHT // 2, 2):
            if heart_equation(real_x, real_y, scale_type):
                screen_x = center_x + real_x  
                screen_y = center_y - real_y
                color = get_fade_color(real_x, real_y)
                heart_data.append(Pos(screen_x + random.randint(-20, 20), screen_y + random.randint(-10, 10), color, real_x, real_y))

def get_hide_pos(heart_data: List[Pos], scale_type: int):
    """
    Generates hidden heart shape positions with slight variations.
    """
    for real_x in range(-WIDTH // 2, WIDTH // 2):
        for real_y in range(-HEIGHT // 2, HEIGHT // 2):
            if heart_equation(real_x, real_y, scale_type):
                screen_x = center_x + real_x
                screen_y = center_y - real_y
                color = get_fade_color(real_x, real_y)
                heart_data.append(Pos(screen_x + random.randint(-5, 5), screen_y + random.randint(-10, 10), color, real_x, real_y))

def generate_falling_particles(heart_data: List[Pos], count: int):
    """
    Generates falling particles from the bottom of the heart shape.
    """
    sorted_heart_data = sorted(heart_data, key=lambda p: p.real_y)  # Sort by height
    bottom_particles = sorted_heart_data[:5000]  # Select lower part of heart
    return [Particle(p.x, p.y, p.color, p.real_x, p.real_y, random.uniform(0, MAX_DELAY)) for p in random.sample(bottom_particles, count)]

def update_falling_particles(particles: List[Particle]):
    """
    Updates the falling effect to ensure continuous particle drops.
    """
    current_time = time.time()
    new_particles = []  

    for p in particles[:]:  
        if not p.active:
            if current_time >= p.start_time:
                p.active = True  
            else:
                continue  

        p.velocity += GRAVITY  
        p.y += p.velocity  

        if p.y > HEIGHT:  
            particles.remove(p)  # Remove particles that have fallen off the screen
            new_particles.append(random.choice(heart_data_root))  # Add new particle
            continue

        screen.set_at((int(p.x), int(p.y)), p.color)

    # Always generate additional new particles
    for p in new_particles:
        particles.append(Particle(p.x, p.y, p.color, p.real_x, p.real_y, random.uniform(0, 1)))


def heart_beat(heart_data: List[Pos], original_heart_data: List[Pos], frame: float) -> None:
    """
    Creates a heartbeat effect with a slow expansion and a fast contraction.
    """
    global out
    t = time.time() * 2  

    # Apply a transformation formula to achieve a slow expansion and fast contraction effect
    if math.sin(t) > 0:
        scale_factor = 1 + 0.06 * math.pow(math.sin(t), 3)  # Slow expansion
    else:
        scale_factor = 1 + 0.06 * math.sin(t)  # Fast contraction

    for i in range(len(heart_data)):
        original_x = original_heart_data[i].real_x
        original_y = original_heart_data[i].real_y

        heart_data[i].real_x = int(original_x * scale_factor) + random.randint(-3, 3)
        heart_data[i].real_y = int(original_y * scale_factor) + random.randint(-3, 3)

        heart_data[i].x = center_x + heart_data[i].real_x
        heart_data[i].y = center_y - heart_data[i].real_y



        




# Initialize heart and particle data
heart_data_root: List[Pos] = []
falling_particles: List[Particle] = []
layout_2: List[Pos] = []

get_pos_begin(heart_data_root, 0)
get_hide_pos(layout_2, 1)
heart_data_root.extend(layout_2)
heart_data = deepcopy(heart_data_root)
falling_particles = generate_falling_particles(heart_data_root, PARTICLE_COUNT)
#update real x,y
for p in heart_data_root:
    p.real_x = p.x - center_x
    p.real_y =  center_y - p.y





pygame.display.flip()

# Main loop
running = True
clock = pygame.time.Clock()

while running:
 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    heart_beat(heart_data,heart_data_root,0)
    
    for p in heart_data:
        screen.set_at((p.x, p.y), p.color)

    update_falling_particles(falling_particles)

    while len(falling_particles) < PARTICLE_COUNT:
        falling_particles.extend(generate_falling_particles(heart_data, 5))

    pygame.display.update()
    

pygame.quit()
