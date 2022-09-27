import pygame

#--------------------------------CONSTANTS---------------------------------#
SCREEN_SIZE = (1980, 1080)
SCREEN_CENTER = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
BACKGROUND_SIZE = (SCREEN_SIZE[0] * 2, SCREEN_SIZE[1] * 2)
BACKGROUND_CENTER = (BACKGROUND_SIZE[0] / 2, BACKGROUND_SIZE[1] / 2)
WAVE_BAR_SIZE = (1000, 20)
WAVE_BAR_LOCATION = (SCREEN_CENTER[0], 1000)
SHOP_TEXT_LOCATION = (600, 200)
COINS_TEXT_LOCATION = (1200, 200)
COINS_NUM_LOCATION = (1350, 200)
PLAYER_HEALTH_BAR_SIZE = (500, 80)
PLAYER_HEALTH_BAR_LOCATION = (370, 50)
STANDARD_BAR_SIZE = (100, 20)
INSIDE_HEALTH_BAR_SIZE = (100, 15)
STANDARD_BAR_GAP = 30
DEFAULT_BAR_MARGIN = 5
INVULNERABILITY_TIME = 288
FRAMERATE = 144
WHITE = (255, 255, 255)
RED = (150, 0, 0)
PURPLE = (150, 0, 150)
GREEN = (0, 150, 0)
BLUE = (0, 0, 150)
BROWN = (150, 100, 0)
CYAN = (0, 150, 150)
BLACK = (0, 0, 0)
SPAWN_COOLDOWN = 100
PLAYER_PROPERTIES = {"size":(100, 100), "speed":5, "health":10, "color":BLUE}
RUNNER_PROPERTIES = {"size":(75, 75), "speed":4, "health":5, "color":RED, "movement_type":"follow", "gun_type":None, "enemy_type":"Runner"}
SHOOTER_PROPERTIES = {"size":(50, 50), "speed":1, "health":5, "color":PURPLE, "movement_type":"default", "gun_type":"Pistol", "enemy_type":"Shooter"}
GIANT_PROPERTIES = {"size":(500, 500), "speed":2, "health":50, "color":BROWN, "movement_type":"follow", "gun_type":None, "enemy_type":"Giant"}
HEAVY_PROPERTIES = {"size":(150, 150), "speed":1, "health":20, "color":CYAN, "movement_type":"default", "gun_type":"Minigun", "enemy_type":"Heavy"}

GUN_PROPERTIES =    {
					    "Pistol":{"reload_cooldown":144, "magazine_size":10, "storage_size":100, "cooldown":100},
					    "M16":{"reload_cooldown":250, "magazine_size":30, "storage_size":200, "cooldown":20},
					    "Sniper":{"reload_cooldown":144, "magazine_size":1, "storage_size":10, "cooldown":200},
					    "Minigun":{"reload_cooldown":500, "magazine_size":200, "storage_size":400, "cooldown":10}
				    }

BULLET_PROPERTIES = {
						"Pistol":{"speed":10, "size":(20, 20), "color":WHITE, "damage":1},
						"M16":{"speed":20, "size":(20, 20), "color":WHITE, "damage":1},
						"Sniper":{"speed":60, "size":(30, 30), "color":WHITE, "damage":5},
						"Minigun":{"speed":15, "size":(20, 20), "color":WHITE, "damage":1}
                    }

#---------------------------------SURFACES---------------------------------#
game_end_surf = pygame.Surface(SCREEN_SIZE)
game_end_surf.fill(RED)
SHOP_WINDOW_SURF = pygame.Surface((1200, 900))

#-----------------------------------RECT-----------------------------------#
BACKGROUND_RECT = pygame.Rect((0, 0), BACKGROUND_SIZE)
SCREEN_PLAYER_RECT = pygame.Rect((0, 0), PLAYER_PROPERTIES["size"])
SCREEN_PLAYER_RECT.center = SCREEN_CENTER
SHOP_WINDOW_RECT = SHOP_WINDOW_SURF.get_rect(center=SCREEN_CENTER)