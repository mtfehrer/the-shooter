import pygame, random, json
import core_funcs as cf
from constants import *

class Entity(pygame.sprite.Sprite):
	def __init__(self, size, pos, speed, color):
		super().__init__()
		self.image = pygame.Surface(size)
		self.image.fill(color)
		self.rect = self.image.get_rect(center=pos)
		self.speed = speed

	def move(self):
		self.rect.x += self.movement[0] * self.speed
		self.rect.y += self.movement[1] * self.speed

	def update(self):
		self.move()

class Background(Entity):
	def __init__(self):
		super().__init__(BACKGROUND_SIZE, SCREEN_CENTER, PLAYER_PROPERTIES["speed"], GREEN)

	def update(self, player_movement):
		self.image.fill(GREEN)
		self.movement = [-player_movement[0], -player_movement[1]]
		self.move()

class Mob(Entity):
	def __init__(self, size, pos, speed, color, health, player=False):
		super().__init__(size, pos, speed, color)
		self.health = health
		if player:
			self.healthbar = Bar(PLAYER_HEALTH_BAR_SIZE, RED, self.health)
		else:
			self.healthbar = Bar(STANDARD_BAR_SIZE, RED, self.health)

class Bar:
	def __init__(self, outside_rect_size, color, max_capacity):
		inside_rect_size = (outside_rect_size[0], outside_rect_size[1] - DEFAULT_BAR_MARGIN)
		self.back_surf = pygame.Surface(outside_rect_size)
		self.back_rect = pygame.Rect((0, 0), outside_rect_size)
		self.front_surf = pygame.Surface(inside_rect_size)
		self.front_surf.fill(color)
		self.front_rect = pygame.Rect((0, 0), inside_rect_size)
		self.front_rect.center = (0, self.back_surf.get_height() / 2)
		self.max_capacity = max_capacity

	def update(self, pos, new_amount):
		self.back_surf.fill(BLACK)
		self.back_rect.center = pos
		self.front_rect.x = ((new_amount / self.max_capacity) * self.front_surf.get_width()) - self.front_surf.get_width()

	def draw(self, screen):
		self.back_surf.blit(self.front_surf, self.front_rect)
		screen.blit(self.back_surf, self.back_rect)

class Wave:
	def __init__(self):
		with open("waves.json") as f:
			self.all_waves = json.load(f)
		self.peace = True
		self.current_wave_num = 0
		self.spawn_cooldown = SPAWN_COOLDOWN

	def next_wave(self):
		self.peace = False
		self.current_wave_num += 1
		self.current_wave = self.all_waves[str(self.current_wave_num)]
		self.enemy_total = 0
		for amount in self.current_wave.values():
			self.enemy_total += amount
		self.bar = Bar(WAVE_BAR_SIZE, RED, self.enemy_total)

	def check_for_clear(self):
		if self.enemy_total == 0:
			self.peace = True
			return True

	def spawn_enemy(self, background_screen_rect):
		self.spawn_cooldown -= 1
		if self.spawn_cooldown <= 0:
			self.spawn_cooldown = SPAWN_COOLDOWN
			num = random.randint(0, 20)
			if num <= 10 and self.current_wave["Runner"] > 0:
				self.current_wave["Runner"] -= 1
				return Enemy(RUNNER_PROPERTIES, background_screen_rect)
			elif num <= 18 and self.current_wave["Shooter"] > 0:
				self.current_wave["Shooter"] -= 1
				return Enemy(SHOOTER_PROPERTIES, background_screen_rect)
			elif num == 19 and self.current_wave["Giant"] > 0:
				self.current_wave["Giant"] -= 1
				return Enemy(GIANT_PROPERTIES, background_screen_rect)
			elif num == 20 and self.current_wave["Heavy"] > 0:
				self.current_wave["Heavy"] -= 1
				return Enemy(HEAVY_PROPERTIES, background_screen_rect)

class Shop:
	def __init__(self, score_font):
		self.score_font = score_font
		self.items = ["M16 - Cost: 20 Coins", "Sniper - Cost: 30 Coins", "Minigun - Cost: 50 Coins"]
		pos = [SCREEN_SIZE[0] / 2, 400]
		shop_text_surf = self.score_font.render("Shop", True, WHITE)
		shop_text_rect = shop_text_surf.get_rect(center=SHOP_TEXT_LOCATION)
		coins_surf = self.score_font.render("Coins:", True, WHITE)
		coins_rect = coins_surf.get_rect(center=COINS_TEXT_LOCATION)
		self.text = [[coins_surf, coins_rect, "Coins:", False], [shop_text_surf, shop_text_rect, "Shop", False]]
		for item in self.items:
			list_ = []
			text_surf = self.score_font.render(item, True, WHITE)
			text_rect = text_surf.get_rect(center=pos)
			self.text.append([text_surf, text_rect, item, False])
			pos[1] += 150

	def detect_buy(self, mouse_rect, mouse_press, coins):
		for text in self.text:
			if mouse_rect.colliderect(text[1]):
				text[0].fill(WHITE)
				text[0].blit(self.score_font.render(text[2], True, BLACK), text[1])
				text[3] = True

	def display(self, screen, coins):
		screen.blit(SHOP_WINDOW_SURF, SHOP_WINDOW_RECT)
		for text in self.text:
			screen.blit(text[0], text[1])
			if text[3] == True:
				text[0].fill(BLACK)
				text[0].blit(self.score_font.render(text[2], True, WHITE), text[1])
				text[3] = False
		coin_num_text = self.score_font.render(str(coins), True, WHITE)
		coin_num_rect = coin_num_text.get_rect(center=COINS_NUM_LOCATION)
		screen.blit(coin_num_text, coin_num_rect)


class Bullet(Entity):
	def __init__(self, properties, type_, pos, end_pos):
		self.type = type_
		if self.type == "enemy":
			properties["color"] = BLACK
		super().__init__(properties["size"], pos, properties["speed"], properties["color"])
		self.properties = properties
		self.movement = cf.get_dx_and_dy(pos, end_pos)

class Player(Mob):
	def __init__(self):
		super().__init__(PLAYER_PROPERTIES["size"], BACKGROUND_CENTER, PLAYER_PROPERTIES["speed"], PLAYER_PROPERTIES["color"], PLAYER_PROPERTIES["health"], True)
		self.guns = [Gun("Pistol", True), Gun("M16", True), Gun("Minigun", True), Gun("Sniper", True)]
		self.selected_gun = 0
		self.invulnerability = 0

	def take_damage(self, damage):
		self.health -= damage
		self.invulnerability = INVULNERABILITY_TIME

	def update(self, keys):
		self.movement = cf.get_key_movement(keys)
		start_pos = self.rect.center
		self.move()
		self.rect.clamp_ip(BACKGROUND_RECT)
		end_pos = self.rect.center
		change_in_x = (end_pos[0] - start_pos[0]) / PLAYER_PROPERTIES["speed"]
		change_in_y = (end_pos[1] - start_pos[1]) / PLAYER_PROPERTIES["speed"]
		#this is used to detect movement for the background
		self.change_in_movement = (change_in_x, change_in_y)
		self.healthbar.update(PLAYER_HEALTH_BAR_LOCATION, self.health)
		reload_bar_pos = (self.rect.center[0], self.rect.center[1] + (self.image.get_height() / 2) + STANDARD_BAR_GAP)
		for gun in self.guns:
			gun.reload_bar.update(reload_bar_pos, gun.reload_cooldown)
		if self.invulnerability <= 0:
			self.image.fill(BLUE)
		elif self.invulnerability > 0:
			self.image.fill(WHITE)
		self.invulnerability -= 1

class Enemy(Mob):
	def __init__(self, properties, screen_rect):
		super().__init__(properties["size"], cf.get_random_spawn(screen_rect, properties["size"]), properties["speed"], properties["color"], properties["health"])
		self.gun = Gun(properties["gun_type"])
		self.type = properties["enemy_type"]
		self.movement_type = properties["movement_type"]
		self.movement = [0, 0]
		self.get_random_path()

	def get_random_path(self):
		self.path = [random.randint(-200, 200), random.randint(-200, 200)]

	def determine_default_movement(self):
		if self.path[0] < 0:
			self.path[0] += 1
			self.movement[0] = -1
		elif self.path[0] > 0:
			self.path[0] -= 1
			self.movement[0] = 1
		else:
			self.movement[0] = 0
		if self.path[1] < 0:
			self.path[1] += 1
			self.movement[1] = -1
		elif self.path[1] > 0:
			self.path[1] -= 1
			self.movement[1] = 1
		else:
			self.movement[1] = 0

	def update(self, player_pos):
		if self.movement_type == "follow": self.movement = cf.get_dx_and_dy(self.rect.center, player_pos)
		elif self.movement_type == "default":
			self.determine_default_movement()
			if self.path == [0, 0]:
				self.get_random_path()
		self.move()
		self.rect.clamp_ip(BACKGROUND_RECT)
		healthbar_pos = (self.rect.center[0], self.rect.center[1] + (self.image.get_height() / 2) + STANDARD_BAR_GAP)
		self.healthbar.update(healthbar_pos, self.health)

class Gun:
	def __init__(self, type_, player_gun=False):
		self.type = type_
		if self.type != None:
			self.properties = GUN_PROPERTIES[self.type]
		self.player_gun = player_gun
		if self.player_gun:
			self.storage_ammo = self.properties["storage_size"]
			self.current_magazine = self.properties["magazine_size"]
			self.reload_cooldown = -1
			self.new_ammo = [0, 0]
			self.reload_bar = Bar(STANDARD_BAR_SIZE, WHITE, self.properties["reload_cooldown"])
		self.current_cooldown = 0

	def update_ammo(self):
		self.storage_ammo = self.new_ammo[0]
		self.current_magazine = self.new_ammo[1]

	def reload(self):
		if self.reload_cooldown == -1 and self.storage_ammo > 0:
			if self.storage_ammo >= self.properties["magazine_size"] - self.current_magazine:
				self.new_ammo[0] = self.storage_ammo - self.properties["magazine_size"] + self.current_magazine
				self.new_ammo[1] = self.properties["magazine_size"]
			else:
				self.new_ammo[1] = self.current_magazine + self.storage_ammo
				self.new_ammo[0] = 0
			self.reload_cooldown = self.properties["reload_cooldown"]
			return True

	def update_cooldown_enemy(self):
		if self.current_cooldown <= 0:
			self.current_cooldown = self.properties["cooldown"]
			return True
		self.current_cooldown -= 1

	def update_cooldown_player(self, trigger_press=True):
		if self.reload_cooldown > 0:
			self.reload_cooldown -= 1
		elif self.reload_cooldown == 0:
			self.update_ammo()
			self.reload_cooldown -= 1
		else:
			if self.current_cooldown <= 0 and self.current_magazine > 0:
				if trigger_press:
					self.current_cooldown = self.properties["cooldown"]
					self.current_magazine -= 1
					return True
		self.current_cooldown -= 1