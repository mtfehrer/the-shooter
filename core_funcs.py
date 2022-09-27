import math, random, pygame
from constants import *

def get_dx_and_dy(start_pos, end_pos):
	opp = end_pos[1] - start_pos[1]
	adj = end_pos[0] - start_pos[0]
	angle_in_rad = math.atan2(opp, adj)
	dx = math.cos(angle_in_rad)
	dy = math.sin(angle_in_rad)
	return (dx, dy)

def get_random_spawn(screen_rect, size):
	while True:
		x = random.randint(0, BACKGROUND_SIZE[0] - size[0])
		y = random.randint(0, BACKGROUND_SIZE[1] - size[1])
		new_rect = pygame.Rect((x, y), size)
		if not new_rect.colliderect(screen_rect):
			return (x, y)

def get_key_movement(keys):
	movement = [0, 0]
	if keys[pygame.K_w] == True:
		movement[1] -= 1
	if keys[pygame.K_a] == True:
		movement[0] -= 1
	if keys[pygame.K_s] == True:
		movement[1] += 1
	if keys[pygame.K_d] == True:
		movement[0] += 1
	return movement