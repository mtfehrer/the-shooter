#things to add:
#background
#textures for enemies
#player texture
#enemy death animations
#enemy death sounds
#items that can be picked up
#hit knockback
#different guns: minigun, railgun, pistol, revolver, flamethrower, shotgun, missle launcher, laser
#bosses
#different modes or levels using json files for game attributes
#shop

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
		self.wave = Wave()
		self.shop = Shop(SCORE_FONT)
		self.shop_mode = False
		self.coins = 0

	def get_all_details(self):
		self.background_screen_rect = pygame.Rect((0, 0), SCREEN_SIZE)
		self.background_screen_rect.center = self.player.sprite.rect.center
		self.mouse_pos = pygame.mouse.get_pos()
		self.background_mouse_pos = (self.mouse_pos[0] + self.background_screen_rect[0], self.mouse_pos[1] + self.background_screen_rect[1])
		self.mouse_press = pygame.mouse.get_pressed()
		self.mouse_rect = pygame.Rect(self.mouse_pos, (1, 1))
		self.keys = pygame.key.get_pressed()

	def handle_shop(self):
		self.shop.detect_buy(self.mouse_rect, self.mouse_press[0], self.coins)

	def handle_wave(self):
		if self.wave.peace == False:
			return_value = self.wave.spawn_enemy(self.background_screen_rect)
			if return_value != None:
				self.enemy_group.add(return_value)
			if self.wave.check_for_clear():
				FINISH_WAVE_SOUND.play()

	def open_shop(self):
		if self.shop_mode == True:
			self.shop_mode = False
		elif self.shop_mode == False:
			self.shop_mode = True

	def enemy_loop(self):
		for enemy in self.enemy_group.sprites():
			self.determine_enemy_shoot(enemy)
			self.determine_enemy_and_player_collision(enemy)
			self.determine_enemy_death(enemy)

	def determine_enemy_shoot(self, enemy):
		if enemy.rect.colliderect(self.background_screen_rect):
			if enemy.gun.type != None:
				if enemy.gun.update_cooldown_enemy():
					self.bullet_group.add(Bullet(BULLET_PROPERTIES[enemy.gun.type], "enemy", enemy.rect.center, self.player.sprite.rect.center))
					GUN_SOUNDS[enemy.gun.type].play()

	def determine_enemy_and_player_collision(self, enemy):
		if self.player.sprite.invulnerability <= 0:
			if enemy.rect.colliderect(self.player.sprite.rect):
				enemy.health -= 1
				self.player.sprite.take_damage(1)
				TAKE_DAMAGE_SOUND.play()

	def determine_enemy_death(self, enemy):
		if enemy.health <= 0:
			if enemy.type == "Runner":
				self.coins += 1
			elif enemy.type == "Shooter":
				self.coins += 2
			elif enemy.type == "Giant" or enemy.type == "Heavy":
				self.coins += 20
			self.enemy_group.remove(enemy)
			self.wave.enemy_total -= 1

	def player_shoot(self):
		if self.shop_mode == False:
			if self.player.sprite.guns[self.player.sprite.selected_gun].update_cooldown_player(self.mouse_press[0]):
				self.bullet_group.add(Bullet(BULLET_PROPERTIES[self.player.sprite.guns[self.player.sprite.selected_gun].type], "player", self.player.sprite.rect.center, self.background_mouse_pos))
				GUN_SOUNDS[self.player.sprite.guns[self.player.sprite.selected_gun].type].play()

	def player_reload(self):
		if self.player.sprite.guns[self.player.sprite.selected_gun].reload():
			RELOAD_SOUND.play()

	def bullet_loop(self):
		for bullet in self.bullet_group.sprites():
			self.determine_bullet_hit(bullet)
			self.delete_out_of_bounds_bullets(bullet)

	def determine_bullet_hit(self, bullet):
		if bullet.type == "player":
			for enemy in self.enemy_group.sprites():
				if bullet.rect.colliderect(enemy.rect):
					enemy.health -= bullet.properties["damage"]
					self.bullet_group.remove(bullet)
					INFLICT_DAMAGE_SOUND.play()
		else:
			if bullet.rect.colliderect(self.player.sprite.rect):
				if self.player.sprite.invulnerability <= 0:
					self.player.sprite.take_damage(bullet.properties["damage"])
					TAKE_DAMAGE_SOUND.play()
				self.bullet_group.remove(bullet)
				
	def delete_out_of_bounds_bullets(self, bullet):
		if (bullet.rect.x < 0 or bullet.rect.x > BACKGROUND_SIZE[0] or 
			bullet.rect.y < 0 or bullet.rect.y > BACKGROUND_SIZE[1]):
			self.bullet_group.remove(bullet)

	def update_all(self):
		self.enemy_group.update(self.player.sprite.rect.center)
		self.bullet_group.update()
		self.player.update(self.keys)
		self.background.update(self.player.sprite.change_in_movement)
		if self.wave.peace == False:
			self.wave.bar.update(WAVE_BAR_LOCATION, self.wave.enemy_total)

	def draw_all(self):
		self.bullet_group.draw(self.background.sprite.image)
		self.enemy_group.draw(self.background.sprite.image)
		self.player.draw(self.background.sprite.image)
		for enemy in self.enemy_group.sprites():
			enemy.healthbar.draw(self.background.sprite.image)
		if self.player.sprite.guns[self.player.sprite.selected_gun].reload_cooldown > 0:
			self.player.sprite.guns[self.player.sprite.selected_gun].reload_bar.draw(self.background.sprite.image)
		self.background.draw(screen)
		self.player.sprite.healthbar.draw(screen)
		if self.wave.peace == False:
			self.wave.bar.draw(screen)

	def display_text(self):
		screen.blit(HEALTH_TEXT, (0, 0))

		weapon_text = SCORE_FONT.render(self.player.sprite.guns[self.player.sprite.selected_gun].type, True, WHITE)
		screen.blit(weapon_text, (0, 100))
		ammo_string = str(self.player.sprite.guns[self.player.sprite.selected_gun].current_magazine) + "/" + str(self.player.sprite.guns[self.player.sprite.selected_gun].storage_ammo)
		ammo_num_text = SCORE_FONT.render(ammo_string, True, WHITE)
		screen.blit(ammo_num_text, (0, 200))

		if self.wave.peace and self.shop_mode == False:
			start_wave_string = "Press 'ENTER' To Start Wave " + str(self.wave.current_wave_num + 1)
			start_wave_text = SCORE_FONT.render(start_wave_string, True, WHITE)
			start_wave_text_rect = start_wave_text.get_rect(center=(SCREEN_CENTER[0], 900))
			screen.blit(start_wave_text, start_wave_text_rect)
		elif self.wave.peace and self.shop_mode == True:
			self.shop.display(screen, self.coins)
		elif self.wave.peace == False and self.shop_mode == False:
			screen.blit(WAVE_TEXT, (SCREEN_CENTER[0] - 130, 900))
			wave_num_text = SCORE_FONT.render(str(self.wave.current_wave_num), True, WHITE)
			screen.blit(wave_num_text, (SCREEN_CENTER[0] + 85, 900))

	def player_death(self):
		if self.player.sprite.health <= 0:
			EXPLOSION_SOUND.play()
			return True

main = Main()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEWHEEL:
			if main.mode == "game":
				game.player.sprite.selected_gun += event.y
				if game.player.sprite.selected_gun == len(game.player.sprite.guns):
					game.player.sprite.selected_gun = 0
				if game.player.sprite.selected_gun == -1:
					game.player.sprite.selected_gun = len(game.player.sprite.guns) - 1
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
					if game.shop_mode == False:
						main.mode = "title"
				elif event.key == 114:
					if game.shop_mode == False:
						game.player_reload()
				elif event.key == 13:
					if game.shop_mode == False:
						if game.wave.peace:
							game.wave.next_wave()
				elif event.key == 9:
					if game.wave.peace:
						game.open_shop()

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
		game.get_all_details()
		game.handle_shop()
		game.handle_wave()
		game.player_shoot()
		game.enemy_loop()
		game.bullet_loop()
		game.update_all()
		game.draw_all()
		game.display_text()
		if game.player_death() == True:
			main.mode = "game-end"
			main.init_game_end(0)

	elif main.mode == "game-end":
		main.display_game_end()

	pygame.display.update()
	clock.tick(FRAMERATE)