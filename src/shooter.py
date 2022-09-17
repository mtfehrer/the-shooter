import pygame, sys, random, math

screen_size = (1980, 1080)
screen_center = (screen_size[0] / 2, screen_size[1] / 2)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
framerate = 144
white = (255, 255, 255)
red = (150, 0, 0)
purple = (150, 0, 150)
green = (0, 150, 0)
blue = (0, 0, 150)
brown = (150, 100, 0)
cyan = (0, 150, 150)
black = (0, 0, 0)
player_speed = 5
player_bullet_speed = 20
player_bullet_size = (20, 20)
player_bullet_cooldown = 10
player_size = (100, 100)
player_health = 20
screen_player_rect = pygame.Rect((0, 0), player_size)
screen_player_rect.center = screen_center
background_size = (screen_size[0] * 2, screen_size[1] * 2)
background_center = (background_size[0] / 2, background_size[1] / 2)
spawn_cooldown = 100
enemy_bullet_speed = 10
enemy_bullet_size = (20, 20)
runner_health = 5
runner_size = (75, 75)
runner_color = red
runner_speed = 4
shooter_health = 5
shooter_speed = 2
shooter_bullet_cooldown = 100
shooter_color = purple
shooter_size = (50, 50)
giant_health = 50
giant_size = (500, 500)
giant_speed = 2
giant_color = brown
heavy_health = 20
heavy_size = (150, 150)
heavy_bullet_cooldown = 10
heavy_speed = 1
heavy_color = cyan
health_bar_size = (100, 20)
inside_health_bar_size = (100, 15)
health_bar_gap = 30
game_end_surf = pygame.Surface(screen_size)
game_end_surf.fill(red)
pygame.init()

title_font = pygame.font.SysFont("consolas", 100)
default_font = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont("comicsansms", 70)

title_text = title_font.render("The Shooter", True, white)
title_text_rect = title_text.get_rect(center=screen_center)
press_space_text = default_font.render("Press 'SPACE' to begin", True, white)
press_space_text_rect = press_space_text.get_rect(center=(screen_center[0], 800))
press_esc_text = default_font.render("Press 'ESC' to exit", True, white)
press_esc_text_rect = press_esc_text.get_rect(center=(screen_center[0], 900))
rules_text = default_font.render("WASD to move, Left Click to shoot", True, white)
rules_text_rect = rules_text.get_rect(center=(screen_center[0], 700))
you_died_text = title_font.render("You Died", True, white)
you_died_text_rect = you_died_text.get_rect(center=screen_center)
retry_text = default_font.render("Press 'SPACE' to retry", True, white)
retry_text_rect = retry_text.get_rect(center=(screen_center[0], 800))
return_to_title_text = default_font.render("Press 'ESC' to return to title", True, white)
return_to_title_text_rect = return_to_title_text.get_rect(center=(screen_center[0], 900))
score_text = score_font.render("Score:", True, white)

pygame.mixer.init()
pygame.mixer.set_num_channels(100)

take_damage_sound = pygame.mixer.Sound("minecrafthit.mp3")
inflict_damage_sound = pygame.mixer.Sound("hitmarker.mp3")
explosion_sound = pygame.mixer.Sound("explosion.mp3")
gun_sound1 = pygame.mixer.Sound("gun1.mp3")
gun_sound1.set_volume(0.2)
gun_sound2 = pygame.mixer.Sound("gun2.mp3")
gun_sound2.set_volume(0.2)
gun_sound3 = pygame.mixer.Sound("gun3.mp3")
gun_sound3.set_volume(0.2)
gun_sound4 = pygame.mixer.Sound("gun4.mp3")
gun_sound4.set_volume(0.2)

class Main:
	def __init__(self):
		self.mode = "title"

	def display_title(self):
		screen.fill(cyan)
		screen.blit(rules_text, rules_text_rect)
		screen.blit(title_text, title_text_rect)
		screen.blit(press_space_text, press_space_text_rect)
		screen.blit(press_esc_text, press_esc_text_rect)

	def init_game_end(self, score):
		self.alpha_level = 0
		string = "Score: " + str(score)
		self.final_score_text = default_font.render(string, True, white)
		self.final_score_text_rect = self.final_score_text.get_rect(center=(screen_center[0], 700))

	def display_game_end(self):
		if self.alpha_level < 30:
			game_end_surf.set_alpha(int(self.alpha_level))
			self.alpha_level += 0.3
			screen.blit(game_end_surf, (0, 0))
		else:
			screen.fill(red)
			screen.blit(you_died_text, you_died_text_rect)
			screen.blit(self.final_score_text, self.final_score_text_rect)
			screen.blit(retry_text, retry_text_rect)
			screen.blit(return_to_title_text, return_to_title_text_rect)

class Game:
	def __init__(self):
		self.background = pygame.sprite.GroupSingle()
		self.background.add(Background())
		self.player = pygame.sprite.GroupSingle()
		self.player.add(Player())
		self.bullet_group = pygame.sprite.Group()
		self.enemy_group = pygame.sprite.Group()
		self.direction = [0, 0]
		self.current_bullet_cooldown = player_bullet_cooldown
		self.current_spawn_cooldown = spawn_cooldown
		self.score = 0

	def get_screen_rect(self):
		self.background_screen_rect = pygame.Rect((0, 0), screen_size)
		self.background_screen_rect.center = self.player.sprite.rect.center

	def move(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w] == True and screen_player_rect.top > self.background.sprite.rect.top:
			self.direction[1] -= player_speed
		if keys[pygame.K_a] == True and screen_player_rect.left > self.background.sprite.rect.left:
			self.direction[0] -= player_speed
		if keys[pygame.K_s] == True and screen_player_rect.bottom < self.background.sprite.rect.bottom:
			self.direction[1] += player_speed
		if keys[pygame.K_d] == True and screen_player_rect.right < self.background.sprite.rect.right:
			self.direction[0] += player_speed

	def player_shoot(self):
		if pygame.mouse.get_pressed()[0] == True and self.current_bullet_cooldown <= 0:
			self.bullet_group.add(PlayerBullet(self.player.sprite.rect.center))
			self.current_bullet_cooldown = player_bullet_cooldown
			gun_sound1.play()
		self.current_bullet_cooldown -= 1

	def enemy_shoot(self):
		for enemy in self.enemy_group.sprites():
			if enemy.rect.colliderect(self.background_screen_rect):
				if str(enemy) == "<Shooter Sprite(in 1 groups)>":
					if enemy.current_bullet_cooldown == 0:
						self.bullet_group.add(EnemyBullet(self.player.sprite.rect.center, enemy.rect.center))
						enemy.current_bullet_cooldown = shooter_bullet_cooldown
						gun_sound3.play()
					enemy.current_bullet_cooldown -= 1
				elif str(enemy) == "<Heavy Sprite(in 1 groups)>":
					if enemy.current_bullet_cooldown == 0:
						self.bullet_group.add(EnemyBullet(self.player.sprite.rect.center, enemy.rect.center))
						enemy.current_bullet_cooldown = heavy_bullet_cooldown
						gun_sound4.play()
					enemy.current_bullet_cooldown -= 1

	def del_bullets(self):
		for bullet in self.bullet_group.sprites():
			if (bullet.rect.x < 0 or bullet.rect.x > background_size[0] or 
			    bullet.rect.y < 0 or bullet.rect.y > background_size[1]):
				self.bullet_group.remove(bullet)

	def spawn_enemies(self):
		if self.current_spawn_cooldown <= 0:
			num = random.randint(0, 50)
			if num <= 30:
				enemy = Runner(self.background_screen_rect)
			elif num <= 48:
				enemy = Shooter(self.background_screen_rect)
			elif num == 49:
				enemy = Giant(self.background_screen_rect)
			elif num == 50:
				enemy = Heavy(self.background_screen_rect)
			self.enemy_group.add(enemy)
			self.current_spawn_cooldown = spawn_cooldown
		self.current_spawn_cooldown -= 1

	def bullet_hit(self):
		for bullet in self.bullet_group.sprites():
			if str(bullet) == "<PlayerBullet Sprite(in 1 groups)>":
				for enemy in self.enemy_group.sprites():
					if bullet.rect.colliderect(enemy.rect):
						enemy.health_bar.sprite.health -= 1
						self.bullet_group.remove(bullet)
						inflict_damage_sound.play()
			else:
				if bullet.rect.colliderect(self.player.sprite.rect):
					self.player.sprite.health_bar.sprite.health -= 1
					self.bullet_group.remove(bullet)
					take_damage_sound.play()

	def player_and_enemy_collision(self):
		for enemy in self.enemy_group.sprites():
			if enemy.rect.colliderect(self.player.sprite.rect):
				enemy.health_bar.sprite.health -= 1
				self.player.sprite.health_bar.sprite.health -= 1
				take_damage_sound.play()

	def kill_enemies(self):
		for enemy in self.enemy_group.sprites():
			if enemy.health_bar.sprite.health <= 0:
				if str(enemy) == "<Runner Sprite(in 1 groups)>":
					self.score += 1
				elif str(enemy) == "<Shooter Sprite(in 1 groups)>":
					self.score += 2
				elif str(enemy) == "<Giant Sprite(in 1 groups)>" or str(enemy) == "<Heavy Sprite(in 1 groups)>":
					self.score += 20
				self.enemy_group.remove(enemy)

	def update_all(self):
		self.enemy_group.update(self.player.sprite.rect.center)
		self.bullet_group.update()
		self.player.update(self.direction)
		self.background.update(self.direction)
		self.direction = [0, 0]

	def draw_all(self):
		self.bullet_group.draw(self.background.sprite.image)
		self.enemy_group.draw(self.background.sprite.image)
		for enemy in self.enemy_group.sprites():
			self.background.sprite.image.blit(enemy.health_bar.sprite.image, enemy.health_bar.sprite.rect)
		self.player.draw(self.background.sprite.image)
		self.background.sprite.image.blit(self.player.sprite.health_bar.sprite.image, self.player.sprite.health_bar.sprite.rect)
		self.background.draw(screen)

	def display_score(self):
		screen.blit(score_text, (0, 0))
		score_num_text = score_font.render(str(self.score), True, white)
		screen.blit(score_num_text, (230, 0))

	def player_death(self):
		if self.player.sprite.health_bar.sprite.health <= 0:
			explosion_sound.play()
			return True

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface(player_size)
		self.image.fill(blue)
		self.rect = self.image.get_rect(center=background_center)
		self.health_bar = pygame.sprite.GroupSingle()
		self.health_bar.add(HealthBar(player_health))

	def move(self, direction):
		self.rect.x += direction[0]
		self.rect.y += direction[1]

	def update(self, direction):
		self.move(direction)
		self.health_bar.update((self.rect.center[0], self.rect.center[1] + (player_size[1] / 2) + health_bar_gap))

class Background(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface(background_size)
		self.rect = self.image.get_rect(center=screen_center)

	def move(self, d):
		self.rect.x -= d[0]
		self.rect.y -= d[1]

	def update(self, d):
		self.move(d)
		self.image.fill(green)

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
			x = random.randint(0, background_size[0] - size[0])
			y = random.randint(0, background_size[1] - size[1])
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
		self.health_bar.update((self.rect.center[0], self.rect.center[1] + (self.arg_dict["size"][1] / 2) + health_bar_gap))

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
			if self.rect.right < background_size[0]:
				self.rect.x += (self.arg_dict["speed"] / 2)
			self.path[0] -= 1
		elif self.path[0] < 0:
			if self.rect.left > 0:
				self.rect.x -= (self.arg_dict["speed"] / 2)
			self.path[0] += 1
		if self.path[1] > 0:
			if self.rect.bottom < background_size[1]:
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
		self.health_bar.update((self.rect.center[0], self.rect.center[1] + (self.arg_dict["size"][1] / 2) + health_bar_gap))

class Runner(RunEnemy):
	def __init__(self, screen_rect):
		super().__init__({"size": runner_size, "color": runner_color, "health": runner_health, "speed": runner_speed, "screen_rect": screen_rect})

class Shooter(ShootEnemy):
	def __init__(self, screen_rect):
		super().__init__({"size": shooter_size, "color": shooter_color, "health": shooter_health, "speed": shooter_speed, "bullet_cooldown": shooter_bullet_cooldown, "screen_rect": screen_rect})

class Giant(RunEnemy):
	def __init__(self, screen_rect):
		super().__init__({"size": giant_size, "color": giant_color, "health": giant_health, "speed": giant_speed, "screen_rect": screen_rect})

class Heavy(ShootEnemy):
	def __init__(self, screen_rect):
		super().__init__({"size": heavy_size, "color": heavy_color, "health": heavy_health, "speed": heavy_speed, "bullet_cooldown": heavy_bullet_cooldown, "screen_rect": screen_rect})

class HealthBar(pygame.sprite.Sprite):
	def __init__(self, health):
		super().__init__()
		self.image = pygame.Surface(health_bar_size)
		self.og_health = health
		self.health = health
	
	def reset_rect(self, pos):
		self.image.fill(black)
		center_x = self.image.get_width() / 2
		center_y = self.image.get_height() / 2
		inside_rect = pygame.Rect((0, 0), inside_health_bar_size)
		inside_rect.center = (0, center_y)
		inside_rect.x = ((self.health / self.og_health) * self.image.get_width()) - self.image.get_width()
		pygame.draw.rect(self.image, red, inside_rect)
		self.rect = self.image.get_rect(center=pos)

	def update(self, pos):
		self.reset_rect(pos)

class PlayerBullet(pygame.sprite.Sprite):
	def __init__(self, player_pos):
		super().__init__()
		self.image = pygame.Surface(player_bullet_size)
		self.image.fill(white)
		self.rect = self.image.get_rect(center=player_pos)
		self.get_dx_and_dy()

	def get_dx_and_dy(self):
		mouse_pos = pygame.mouse.get_pos()
		adj = mouse_pos[0] - screen_center[0]
		opp = mouse_pos[1] - screen_center[1]
		angle_in_rad = math.atan2(opp, adj)
		self.dx = math.cos(angle_in_rad)
		self.dy = math.sin(angle_in_rad)

	def move(self):
		self.rect.x += (self.dx * player_bullet_speed)
		self.rect.y += (self.dy * player_bullet_speed)

	def update(self):
		self.move()

class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, player_pos, enemy_pos):
		super().__init__()
		self.image = pygame.Surface(enemy_bullet_size)
		self.image.fill(black)
		self.rect = self.image.get_rect(center=enemy_pos)
		self.get_dx_and_dy(player_pos, enemy_pos)

	def get_dx_and_dy(self, player_pos, enemy_pos):
		adj = enemy_pos[0] - player_pos[0]
		opp = enemy_pos[1] - player_pos[1]
		angle_in_rad = math.atan2(opp, adj)
		self.dx = math.cos(angle_in_rad)
		self.dy = math.sin(angle_in_rad)

	def move(self):
		self.rect.x -= (self.dx * enemy_bullet_speed)
		self.rect.y -= (self.dy * enemy_bullet_speed)

	def update(self):
		self.move()

main = Main()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if main.mode == "title":
				if event.key == 27:
					pygame.quit()
					sys.exit()
				if event.key == 32:
					main.mode = "game"
					game = Game()

			elif main.mode == "game":
				if event.key == 27:
					main.mode = "title"

			elif main.mode == "game-end":
				if event.key == 27:
					main.mode = "title"
				elif event.key == 32:
					main.mode = "game"
					game = Game()

	if main.mode == "title":
		main.display_title()

	elif main.mode == "game":
		screen.fill(black)
		game.get_screen_rect()
		game.spawn_enemies()
		game.move()
		game.player_shoot()
		game.enemy_shoot()
		game.del_bullets()
		game.bullet_hit()
		game.player_and_enemy_collision()
		game.kill_enemies()
		game.update_all()
		game.draw_all()
		game.display_score()
		if game.player_death() == True:
			main.mode = "game-end"
			main.init_game_end(game.score)

	elif main.mode == "game-end":
		main.display_game_end()

	pygame.display.update()
	clock.tick(framerate)