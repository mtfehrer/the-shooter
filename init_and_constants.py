from constants import *
import pygame

#----------------------------------FONTS-----------------------------------#
pygame.font.init()
TITLE_FONT = pygame.font.SysFont("consolas", 100)
DEFAULT_FONT = pygame.font.SysFont(None, 50)
SCORE_FONT = pygame.font.SysFont("comicsansms", 70)

#------------------------------TEXT AND RECT-------------------------------#
TITLE_TEXT = TITLE_FONT.render("The Shooter", True, WHITE)
TITLE_TEXT_RECT = TITLE_TEXT.get_rect(center=SCREEN_CENTER)
PRESS_SPACE_TEXT = DEFAULT_FONT.render("Press 'SPACE' to begin", True, WHITE)
PRESS_SPACE_TEXT_RECT = PRESS_SPACE_TEXT.get_rect(center=(SCREEN_CENTER[0], 800))
PRESS_ESC_TEXT = DEFAULT_FONT.render("Press 'ESC' to exit", True, WHITE)
PRESS_ESC_TEXT_RECT = PRESS_ESC_TEXT.get_rect(center=(SCREEN_CENTER[0], 900))
RULES_TEXT = DEFAULT_FONT.render("WASD to move, Left Click to shoot", True, WHITE)
RULES_TEXT_RECT = RULES_TEXT.get_rect(center=(SCREEN_CENTER[0], 700))
YOU_DIED_TEXT = TITLE_FONT.render("You Died", True, WHITE)
YOU_DIED_TEXT_RECT = YOU_DIED_TEXT.get_rect(center=SCREEN_CENTER)
RETRY_TEXT = DEFAULT_FONT.render("Press 'SPACE' to retry", True, WHITE)
RETRY_TEXT_RECT = RETRY_TEXT.get_rect(center=(SCREEN_CENTER[0], 800))
RETURN_TO_TITLE_TEXT = DEFAULT_FONT.render("Press 'ESC' to return to title", True, WHITE)
RETURN_TO_TITLE_TEXT_RECT = RETURN_TO_TITLE_TEXT.get_rect(center=(SCREEN_CENTER[0], 900))
HEALTH_TEXT = SCORE_FONT.render("HP:", True, WHITE)
WAVE_TEXT = SCORE_FONT.render("Wave: ", True, WHITE)

#----------------------------------SOUND-----------------------------------#
pygame.mixer.init()
pygame.mixer.set_num_channels(100)
FINISH_WAVE_SOUND = pygame.mixer.Sound("sfx/beep.mp3")
TAKE_DAMAGE_SOUND = pygame.mixer.Sound("sfx/minecrafthit.mp3")
INFLICT_DAMAGE_SOUND = pygame.mixer.Sound("sfx/hitmarker.mp3")
EXPLOSION_SOUND = pygame.mixer.Sound("sfx/explosion.mp3")
RELOAD_SOUND = pygame.mixer.Sound("sfx/reload.mp3")
M16_SOUND = pygame.mixer.Sound("sfx/gun1.mp3")
M16_SOUND.set_volume(0.2)
GUN_SOUND2 = pygame.mixer.Sound("sfx/gun2.mp3")
GUN_SOUND2.set_volume(0.2)
PISTOL_SOUND = pygame.mixer.Sound("sfx/gun3.mp3")
PISTOL_SOUND.set_volume(0.2)
MINIGUN_SOUND = pygame.mixer.Sound("sfx/gun4.mp3")
MINIGUN_SOUND.set_volume(0.2)
SNIPER_SOUND = pygame.mixer.Sound("sfx/sniper.mp3")
SNIPER_SOUND.set_volume(1)
GUN_SOUNDS = {"Pistol":PISTOL_SOUND, "M16":M16_SOUND, "Sniper":SNIPER_SOUND, "Minigun":MINIGUN_SOUND}

#----------------------------------PYGAME----------------------------------#
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.event.set_grab(True)
pygame.init()