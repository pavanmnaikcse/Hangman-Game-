import pygame
import sys
from settings import *

def map_mouse_pos(pos, current_w, current_h):
    ratio = min(current_w / WIDTH, current_h / HEIGHT)
    scaled_w = int(WIDTH * ratio)
    scaled_h = int(HEIGHT * ratio)
    x_offset = (current_w - scaled_w) // 2
    y_offset = (current_h - scaled_h) // 2
    
    internal_x = (pos[0] - x_offset) / ratio
    internal_y = (pos[1] - y_offset) / ratio
    return (int(internal_x), int(internal_y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Dark Hangman")
    
    game_surface = pygame.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    from game_state import GameState
    game = GameState()
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        events = pygame.event.get()
        current_w, current_h = screen.get_size()
        
        modified_events = []
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                if hasattr(event, 'pos'):
                    event.pos = map_mouse_pos(event.pos, current_w, current_h)
            modified_events.append(event)
            
        mapped_mouse = map_mouse_pos(pygame.mouse.get_pos(), current_w, current_h)
                
        if not game.update(dt, modified_events, mouse_pos=mapped_mouse):
            running = False
            
        # Draw everything onto the internal surface
        game.draw(game_surface)
        
        # Scale internal surface to fit screen
        ratio = min(current_w / WIDTH, current_h / HEIGHT)
        scaled_w = int(WIDTH * ratio)
        scaled_h = int(HEIGHT * ratio)
        scaled_surface = pygame.transform.scale(game_surface, (scaled_w, scaled_h))
        
        screen.fill((0, 0, 0)) # black borders
        x_offset = (current_w - scaled_w) // 2
        y_offset = (current_h - scaled_h) // 2
        screen.blit(scaled_surface, (x_offset, y_offset))
        
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
