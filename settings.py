import pygame

# Screen settings
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Colors (Dark Fantasy Theme)
BG_COLOR = (10, 10, 15)          # Deep dark night
TEXT_COLOR = (220, 220, 200)     # Parchment white
HIGHLIGHT_COLOR = (200, 150, 50) # Gold / Fire highlight
ERROR_COLOR = (150, 30, 30)      # Blood red / Dark red
MENU_BG_COLOR = (20, 20, 25)

# Game logic settings
MAX_ATTEMPTS = 6
COUNTDOWN_TIME = 60  # seconds per word

# Fonts (we'll use Pygame default if custom ones aren't loaded)
FONT_NAME = 'freesansbold.ttf'
TITLE_FONT_SIZE = 80
MENU_FONT_SIZE = 40
HUD_FONT_SIZE = 30
WORD_FONT_SIZE = 60

# Visual effects settings
FOG_DENSITY = 100
MAX_PARTICLES = 200
RAIN_DROPS = 150
