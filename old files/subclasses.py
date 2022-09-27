import pygame, math, random
from constants import *

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface(PLAYER_SIZE)
		self.image.fill(BLUE)
		self.rect = self.image.get_rect(center=BACKGROUND_CENTER)
		self.health_bar = pygame.sprite.GroupSingle()
		self.health_bar.add(HealthBar(PLAYER_HEALTH))

	def move(self, direction):
		self.rect.x += direction[0]
		self.rect.y += direction[1]

	def update(self, direction):
		self.move(direction)
		self.health_bar.update((self.rect.center[0], self.rect.center[1] + (PLAYER_SIZE[1] / 2) + HEALTH_BAR_GAP))

class Background(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface(BACKGROUND_SIZE)
		self.rect = self.image.get_rect(center=SCREEN_CENTER)

	def move(self, direction):
		self.rect.x -= direction[0]
		self.rect.y -= direction[1]

	def update(self, direction):
		self.move(direction)
		self.image.fill(GREEN)

class Enemy(pygame.sprite.Sprite):
	def __init__(self, arg_dict):
		super().__init__()
		self.arg_dict = arg_dict
		self.image = pygame.Surface(arg_dict["size"])
		self.image.fill(arg_dict["color"])
		self.get_spawn_pos(arg_dict["screen_rect"], arg_dict["size"])
		self.health_bar = pygame.sprite.GroupSingle()
		self.health_bar.add(HealthBar(arg_dict["health"]))

	def get_spawn_pos(self, screen_rect, size):
		while True:
			x = random.randint(0, BACKGROUND_SIZE[0] - size[0])
			y = random.randint(0, BACKGROUND_SIZE[1] - size[1])
			self.rect = self.image.get_rect(topleft=(x, y))
			if not self.rect.colliderect(screen_rect):
				break

class RunEnemy(Enemy):
	def __init__(self, arg_dict):
		super().__init__(arg_dict)

	def get_dx_and_dy(self, player_pos):
		adj = player_pos[0] - self.rect.center[0]
		opp = player_pos[1] - self.rect.center[1]
		angle_in_deg = math.atan2(opp, adj)
		self.dx = math.cos(angle_in_deg)
		self.dy = math.sin(angle_in_deg)

	def move(self):
		self.rect.x += (self.dx * self.arg_dict["speed"])
		self.rect.y += (self.dy * self.arg_dict["speed"])

	def update(self, player_pos):
		self.get_dx_and_dy(player_pos)
		self.move()
		self.health_bar.update((self.rect.center[0], self.rect.center[1] + (self.arg_dict["size"][1] / 2) + HEALTH_BAR_GAP))

class ShootEnemy(Enemy):
	def __init__(self, arg_dict):
		super().__init__(arg_dict)
		self.reset_path()
		self.og_bullet_cooldown = arg_dict["bullet_cooldown"]
		self.current_bullet_cooldown = arg_dict["bullet_cooldown"]

	def reset_path(self):
		self.path = [random.randint(-100, 100), random.randint(-100, 100)]

	def move(self):
		if self.path[0] > 0:
			if self.rect.right < BACKGROUND_SIZE[0]:
				self.rect.x += (self.arg_dict["speed"] / 2)
			self.path[0] -= 1
		elif self.path[0] < 0:
			if self.rect.left > 0:
				self.rect.x -= (self.arg_dict["speed"] / 2)
			self.path[0] += 1
		if self.path[1] > 0:
			if self.rect.bottom < BACKGROUND_SIZE[1]:
				self.rect.y += (self.arg_dict["speed"] / 2)
			self.path[1] -= 1
		elif self.path[1] < 0:
			if self.rect.top > 0:
				self.rect.y -= (self.arg_dict["speed"] / 2)
			self.path[1] += 1

	def update(self, *args):
		self.move()
		if self.path[0] == 0 and self.path[1] == 0:
			self.reset_path()
		self.health_bar.update((self.rect.center[0], self.rect.center[1] + (self.arg_dict["size"][1] / 2) + HEALTH_BAR_GAP))

class Runner(RunEnemy):
	def __init__(self, screen_rect):
		super().__init__({"size": RUNNER_SIZE, "color": RUNNER_COLOR, "health": RUNNER_HEALTH, "speed": RUNNER_SPEED, "screen_rect": screen_rect})

class Shooter(ShootEnemy):
	def __init__(self, screen_rect):
		super().__init__({"size": SHOOTER_SIZE, "color": SHOOTER_COLOR, "health": SHOOTER_HEALTH, "speed": SHOOTER_SPEED, "bullet_cooldown": SHOOTER_BULLET_COOLDOWN, "screen_rect": screen_rect})

class Giant(RunEnemy):
	def __init__(self, screen_rect):
		super().__init__({"size": GIANT_SIZE, "color": GIANT_COLOR, "health": GIANT_HEALTH, "speed": GIANT_SPEED, "screen_rect": screen_rect})

class Heavy(ShootEnemy):
	def __init__(self, screen_rect):
		super().__init__({"size": HEAVY_SIZE, "color": HEAVY_COLOR, "health": HEAVY_HEALTH, "speed": HEAVY_SPEED, "bullet_cooldown": HEAVY_BULLET_COOLDOWN, "screen_rect": screen_rect})

class HealthBar(pygame.sprite.Sprite):
	def __init__(self, health):
		super().__init__()
		self.image = pygame.Surface(HEALTH_BAR_SIZE)
		self.og_health = health
		self.health = health
	
	def reset_rect(self, pos):
		self.image.fill(BLACK)
		center_x = self.image.get_width() / 2
		center_y = self.image.get_height() / 2
		inside_rect = pygame.Rect((0, 0), INSIDE_HEALTH_BAR_SIZE)
		inside_rect.center = (0, center_y)
		inside_rect.x = ((self.health / self.og_health) * self.image.get_width()) - self.image.get_width()
		pygame.draw.rect(self.image, RED, inside_rect)
		self.rect = self.image.get_rect(center=pos)

	def update(self, pos):
		self.reset_rect(pos)

class PlayerBullet(pygame.sprite.Sprite):
	def __init__(self, player_pos):
		super().__init__()
		self.image = pygame.Surface(PLAYER_BULLET_SIZE)
		self.image.fill(WHITE)
		self.rect = self.image.get_rect(center=player_pos)
		self.get_dx_and_dy()

	def get_dx_and_dy(self):
		mouse_pos = pygame.mouse.get_pos()
		adj = mouse_pos[0] - SCREEN_CENTER[0]
		opp = mouse_pos[1] - SCREEN_CENTER[1]
		angle_in_rad = math.atan2(opp, adj)
		self.dx = math.cos(angle_in_rad)
		self.dy = math.sin(angle_in_rad)

	def move(self):
		self.rect.x += (self.dx * PLAYER_BULLET_SPEED)
		self.rect.y += (self.dy * PLAYER_BULLET_SPEED)

	def update(self):
		self.move()

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, player_pos, enemy_pos):
		super().__init__()
		self.image = pygame.Surface(ENEMY_BULLET_SIZE)
		self.image.fill(BLACK)
		self.rect = self.image.get_rect(center=enemy_pos)
		self.get_dx_and_dy(player_pos, enemy_pos)

	def get_dx_and_dy(self, player_pos, enemy_pos):
		adj = enemy_pos[0] - player_pos[0]
		opp = enemy_pos[1] - player_pos[1]
		angle_in_rad = math.atan2(opp, adj)
		self.dx = math.cos(angle_in_rad)
		self.dy = math.sin(angle_in_rad)

	def move(self):
		self.rect.x -= (self.dx * ENEMY_BULLET_SPEED)
		self.rect.y -= (self.dy * ENEMY_BULLET_SPEED)

	def update(self):
		self.move()