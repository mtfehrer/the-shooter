#things to add:
#background
#limited ammo (it can regen if game is endless)
#delete bullets outside of screen
#items that can be picked up
#textures for enemies
#player texture
#enemy death animations
#enemy death sounds
#hit knockback
#hit invulnerability
#different guns: minigun, railgun, pistol, revolver, flamethrower, shotgun, missle launcher, laser
#bosses
#different modes or levels using json files for game attributes
#waves
#for levels have a bar that shows how many enemies are left

import pygame, random, sys, math
from subclasses import *
from constants import *
from init_and_constants import *

class Main:
	def __init__(self):
		self.mode = "title"

	def display_title(self):
		screen.fill(CYAN)
		screen.blit(RULES_TEXT, RULES_TEXT_RECT)
		screen.blit(TITLE_TEXT, TITLE_TEXT_RECT)
		screen.blit(PRESS_SPACE_TEXT, PRESS_SPACE_TEXT_RECT)
		screen.blit(PRESS_ESC_TEXT, PRESS_ESC_TEXT_RECT)

	def init_game_end(self, score):
		self.alpha_level = 0
		string = "Score: " + str(score)
		self.final_score_text = DEFAULT_FONT.render(string, True, WHITE)
		self.final_score_text_rect = self.final_score_text.get_rect(center=(SCREEN_CENTER[0], 700))

	def display_game_end(self):
		if self.alpha_level < 30:
			game_end_surf.set_alpha(int(self.alpha_level))
			self.alpha_level += 0.3
			screen.blit(game_end_surf, (0, 0))
		else:
			screen.fill(RED)
			screen.blit(YOU_DIED_TEXT, YOU_DIED_TEXT_RECT)
			screen.blit(self.final_score_text, self.final_score_text_rect)
			screen.blit(RETRY_TEXT, RETRY_TEXT_RECT)
			screen.blit(RETURN_TO_TITLE_TEXT, RETURN_TO_TITLE_TEXT_RECT)

class Game:
	def __init__(self):
		self.background = pygame.sprite.GroupSingle()
		self.background.add(Background())
		self.player = pygame.sprite.GroupSingle()
		self.player.add(Player())
		self.bullet_group = pygame.sprite.Group()
		self.enemy_group = pygame.sprite.Group()
		self.direction = [0, 0]
		self.current_bullet_cooldown = PLAYER_BULLET_COOLDOWN
		self.current_spawn_cooldown = SPAWN_COOLDOWN
		self.score = 0

	def get_screen_rect(self):
		self.background_screen_rect = pygame.Rect((0, 0), SCREEN_SIZE)
		self.background_screen_rect.center = self.player.sprite.rect.center

	def move(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w] == True and SCREEN_PLAYER_RECT.top > self.background.sprite.rect.top:
			self.direction[1] -= PLAYER_SPEED
		if keys[pygame.K_a] == True and SCREEN_PLAYER_RECT.left > self.background.sprite.rect.left:
			self.direction[0] -= PLAYER_SPEED
		if keys[pygame.K_s] == True and SCREEN_PLAYER_RECT.bottom < self.background.sprite.rect.bottom:
			self.direction[1] += PLAYER_SPEED
		if keys[pygame.K_d] == True and SCREEN_PLAYER_RECT.right < self.background.sprite.rect.right:
			self.direction[0] += PLAYER_SPEED

	def player_shoot(self):
		if pygame.mouse.get_pressed()[0] == True and self.current_bullet_cooldown <= 0:
			self.bullet_group.add(PlayerBullet(self.player.sprite.rect.center))
			self.current_bullet_cooldown = PLAYER_BULLET_COOLDOWN
			GUN_SOUND1.play()
		self.current_bullet_cooldown -= 1

	def enemy_shoot(self):
		for enemy in self.enemy_group.sprites():
			if enemy.rect.colliderect(self.background_screen_rect):
				if str(enemy) == "<Shooter Sprite(in 1 groups)>":
					if enemy.current_bullet_cooldown == 0:
						self.bullet_group.add(EnemyBullet(self.player.sprite.rect.center, enemy.rect.center))
						enemy.current_bullet_cooldown = SHOOTER_BULLET_COOLDOWN
						GUN_SOUND3.play()
					enemy.current_bullet_cooldown -= 1
				elif str(enemy) == "<Heavy Sprite(in 1 groups)>":
					if enemy.current_bullet_cooldown == 0:
						self.bullet_group.add(EnemyBullet(self.player.sprite.rect.center, enemy.rect.center))
						enemy.current_bullet_cooldown = HEAVY_BULLET_COOLDOWN
						GUN_SOUND4.play()
					enemy.current_bullet_cooldown -= 1

	def del_bullets(self):
		for bullet in self.bullet_group.sprites():
			if (bullet.rect.x < 0 or bullet.rect.x > BACKGROUND_SIZE[0] or 
			    bullet.rect.y < 0 or bullet.rect.y > BACKGROUND_SIZE[1]):
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
			self.current_spawn_cooldown = SPAWN_COOLDOWN
		self.current_spawn_cooldown -= 1

	def bullet_hit(self):
		for bullet in self.bullet_group.sprites():
			if str(bullet) == "<PlayerBullet Sprite(in 1 groups)>":
				for enemy in self.enemy_group.sprites():
					if bullet.rect.colliderect(enemy.rect):
						enemy.health_bar.sprite.health -= 1
						self.bullet_group.remove(bullet)
						INFLICT_DAMAGE_SOUND.play()
			else:
				if bullet.rect.colliderect(self.player.sprite.rect):
					self.player.sprite.health_bar.sprite.health -= 1
					self.bullet_group.remove(bullet)
					TAKE_DAMAGE_SOUND.play()

	def player_and_enemy_collision(self):
		for enemy in self.enemy_group.sprites():
			if enemy.rect.colliderect(self.player.sprite.rect):
				enemy.health_bar.sprite.health -= 1
				self.player.sprite.health_bar.sprite.health -= 1
				TAKE_DAMAGE_SOUND.play()

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
		screen.blit(SCORE_TEXT, (0, 0))
		score_num_text = SCORE_FONT.render(str(self.score), True, WHITE)
		screen.blit(score_num_text, (230, 0))

	def player_death(self):
		if self.player.sprite.health_bar.sprite.health <= 0:
			EXPLOSION_SOUND.play()
			return True

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
		screen.fill(BLACK)
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
	clock.tick(FRAMERATE)