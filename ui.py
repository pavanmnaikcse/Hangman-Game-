import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, font_size=MENU_FONT_SIZE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(FONT_NAME, font_size)
        self.is_hovered = False
        self.hover_progress = 0.0

    def update(self, mouse_pos, dt):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered:
            self.hover_progress = min(1.0, self.hover_progress + dt * 5)
        else:
            self.hover_progress = max(0.0, self.hover_progress - dt * 5)

    def draw(self, surface):
        # Interpolate color
        r = int(MENU_BG_COLOR[0] + (HIGHLIGHT_COLOR[0] - MENU_BG_COLOR[0]) * self.hover_progress)
        g = int(MENU_BG_COLOR[1] + (HIGHLIGHT_COLOR[1] - MENU_BG_COLOR[1]) * self.hover_progress)
        b = int(MENU_BG_COLOR[2] + (HIGHLIGHT_COLOR[2] - MENU_BG_COLOR[2]) * self.hover_progress)
        
        pygame.draw.rect(surface, (r, g, b), self.rect, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, width=2, border_radius=10)

        text_surf = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

def draw_text(surface, text, font_size, x, y, color=TEXT_COLOR, center=True):
    font = pygame.font.SysFont(FONT_NAME, font_size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surf, text_rect)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = TEXT_COLOR
        self.text = text
        self.font = pygame.font.SysFont(FONT_NAME, MENU_FONT_SIZE)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0

    def update(self, dt):
        self.cursor_timer += dt
        if self.cursor_timer > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
        elif event.type == pygame.TEXTINPUT:
            if self.active and len(self.text) < 15:
                self.text += event.text
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, MENU_BG_COLOR, self.rect, border_radius=5)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, self.rect, 2, border_radius=5)
        display_text = self.text + ('|' if self.cursor_visible else '')
        self.txt_surface = self.font.render(display_text, True, self.color)
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)

