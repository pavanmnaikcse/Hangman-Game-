import pygame
from settings import *
from words import get_random_word
from visuals import SceneRenderer
from ui import draw_text, Button, InputBox
from audio import AudioManager

class GameState:
    def __init__(self):
        self.word, self.category = get_random_word()
        self.guessed_letters = set()
        self.mistakes = 0
        self.time_left = COUNTDOWN_TIME
        self.score = 0
        self.state = "NAME_INPUT"
        self.renderer = SceneRenderer()
        self.audio = AudioManager()
        
        self.player_name = ""
        
        btn_w, btn_h = 300, 60
        # Input state
        self.input_box = InputBox(WIDTH//2 - btn_w//2, HEIGHT//2, btn_w, 50)
        self.btn_submit_name = Button(WIDTH//2 - btn_w//2, HEIGHT//2 + 80, btn_w, btn_h, "Continue")
        
        # Menu state
        self.btn_start = Button(WIDTH//2 - btn_w//2, HEIGHT//2 - 40, btn_w, btn_h, "Start Game")
        self.btn_quit = Button(WIDTH//2 - btn_w//2, HEIGHT//2 + 40, btn_w, btn_h, "Exit")
        
        # Instructions state
        self.btn_play = Button(WIDTH//2 - btn_w//2, HEIGHT - 100, btn_w, btn_h, "Play")
        
        # Game Over
        self.btn_restart = Button(WIDTH//2 - btn_w//2, HEIGHT//2 + 100, btn_w, btn_h, "Restart Game")
        
        # Victory
        self.btn_menu = Button(WIDTH//2 - btn_w//2, HEIGHT//2 + 100, btn_w, btn_h, "Back to Menu")

    def reset_game(self):
        self.word, self.category = get_random_word()
        self.guessed_letters = set()
        self.mistakes = 0
        self.time_left = COUNTDOWN_TIME
        self.state = "PLAYING"
        self.renderer = SceneRenderer()

    def guess_letter(self, letter):
        if letter in self.guessed_letters or self.state != "PLAYING":
            return
        
        self.guessed_letters.add(letter)
        self.audio.play("click")
        if letter not in self.word:
            self.mistakes += 1
            self.renderer.trigger_thunder()
            self.audio.play("thunder")
            if self.mistakes >= MAX_ATTEMPTS:
                self.state = "GAME_OVER"
                self.audio.play("loss")
        else:
            if all(char in self.guessed_letters or char == ' ' for char in self.word):
                self.state = "VICTORY"
                self.score += 100 + int(self.time_left)
                self.audio.play("win")

    def update(self, dt, events, mouse_pos=None):
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        
        if self.state == "NAME_INPUT":
            self.renderer.update(dt)
            self.input_box.update(dt)
            self.btn_submit_name.update(mouse_pos, dt)
            for event in events:
                name_ret = self.input_box.handle_event(event)
                if name_ret is not None:
                    self.player_name = name_ret if name_ret.strip() else "Guest"
                    self.audio.play("click")
                    self.state = "MENU"
                if self.btn_submit_name.is_clicked(event):
                    self.player_name = self.input_box.text if self.input_box.text.strip() else "Guest"
                    self.audio.play("click")
                    self.state = "MENU"

        elif self.state == "MENU":
            self.renderer.update(dt)
            self.btn_start.update(mouse_pos, dt)
            self.btn_quit.update(mouse_pos, dt)
            for event in events:
                if self.btn_start.is_clicked(event):
                    self.audio.play("click")
                    self.state = "INSTRUCTIONS"
                if self.btn_quit.is_clicked(event):
                    self.audio.play("click")
                    return False
                    
        elif self.state == "INSTRUCTIONS":
            self.renderer.update(dt)
            self.btn_play.update(mouse_pos, dt)
            for event in events:
                if self.btn_play.is_clicked(event):
                    self.audio.play("click")
                    self.reset_game()
        
        elif self.state == "PLAYING":
            self.renderer.update(dt)
            self.time_left -= dt
            if self.time_left <= 0:
                self.state = "GAME_OVER"
                self.audio.play("loss")
                
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        self.guess_letter(event.unicode.upper())
        
        elif self.state == "GAME_OVER":
            self.renderer.update(dt)
            self.btn_restart.update(mouse_pos, dt)
            for event in events:
                if self.btn_restart.is_clicked(event):
                    self.audio.play("click")
                    self.reset_game()
                    
        elif self.state == "VICTORY":
            self.renderer.update(dt)
            self.btn_menu.update(mouse_pos, dt)
            for event in events:
                if self.btn_menu.is_clicked(event):
                    self.audio.play("click")
                    self.state = "MENU"
                    self.score = 0
                    
        return True

    def draw(self, surface):
        if self.state == "NAME_INPUT":
            self.renderer.draw(surface, 0)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (0, 0))
            draw_text(surface, "DARK HANGMAN", TITLE_FONT_SIZE, WIDTH//2, HEIGHT//3)
            draw_text(surface, "Enter your name, brave soul:", MENU_FONT_SIZE, WIDTH//2, HEIGHT//2 - 40)
            self.input_box.draw(surface)
            self.btn_submit_name.draw(surface)

        elif self.state == "MENU":
            self.renderer.draw(surface, 0)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (0, 0))
            
            draw_text(surface, "DARK HANGMAN", TITLE_FONT_SIZE, WIDTH//2, HEIGHT//3)
            draw_text(surface, f"Welcome, {self.player_name}", HUD_FONT_SIZE, WIDTH//2, HEIGHT//3 + 60, HIGHLIGHT_COLOR)
            self.btn_start.draw(surface)
            self.btn_quit.draw(surface)
            
        elif self.state == "INSTRUCTIONS":
            self.renderer.draw(surface, 0)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            surface.blit(overlay, (0, 0))
            
            draw_text(surface, "HOW TO PLAY", TITLE_FONT_SIZE, WIDTH//2, HEIGHT//4)
            inst = [
                "1. Type letters on your keyboard to guess the hidden word.",
                "2. Each wrong guess brings you closer to the gallows.",
                "3. You have 6 attempts and 60 seconds per word.",
                "4. Survive to earn points based on time remaining.",
                "May the shadows spare you."
            ]
            for i, line in enumerate(inst):
                draw_text(surface, line, HUD_FONT_SIZE, WIDTH//2, HEIGHT//2 - 50 + i*40)
                
            self.btn_play.draw(surface)

        elif self.state == "PLAYING":
            self.renderer.draw(surface, self.mistakes)
            
            # HUD
            draw_text(surface, f"Player: {self.player_name}", HUD_FONT_SIZE, 100, 30, center=False)
            draw_text(surface, f"Category: {self.category}", HUD_FONT_SIZE, WIDTH//2, 30)
            draw_text(surface, f"Score: {self.score}", HUD_FONT_SIZE, 100, 70, center=False)
            draw_text(surface, f"Time: {int(self.time_left)}", HUD_FONT_SIZE, WIDTH - 150, 30, center=False)
            draw_text(surface, f"Attempts: {MAX_ATTEMPTS - self.mistakes}/{MAX_ATTEMPTS}", HUD_FONT_SIZE, WIDTH - 180, 70, center=False)
            
            # Word display
            display_word = ""
            for char in self.word:
                if char in self.guessed_letters or char == ' ':
                    display_word += char + " "
                else:
                    display_word += "_ "
            draw_text(surface, display_word.strip(), WORD_FONT_SIZE, WIDTH//2, HEIGHT - 100)
            
            # Guessed letters
            wrong_letters = [l for l in self.guessed_letters if l not in self.word]
            draw_text(surface, "Misses: " + " ".join(wrong_letters), HUD_FONT_SIZE, WIDTH//2, HEIGHT - 40, ERROR_COLOR)
            
        elif self.state == "GAME_OVER":
            self.renderer.draw(surface, MAX_ATTEMPTS)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((150, 0, 0, 200)) # Strong red tint
            surface.blit(overlay, (0, 0))
            
            draw_text(surface, "YOU DIED", TITLE_FONT_SIZE, WIDTH//2, HEIGHT//3 - 30, (255, 50, 50))
            draw_text(surface, f"The word was: {self.word}", MENU_FONT_SIZE, WIDTH//2, HEIGHT//2 - 20, (255, 200, 200))
            self.btn_restart.draw(surface)
            
        elif self.state == "VICTORY":
            self.renderer.draw(surface, self.mistakes)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 50, 0, 180))
            surface.blit(overlay, (0, 0))
            
            draw_text(surface, "SURVIVED", TITLE_FONT_SIZE, WIDTH//2, HEIGHT//3, HIGHLIGHT_COLOR)
            draw_text(surface, f"Score: {self.score}", MENU_FONT_SIZE, WIDTH//2, HEIGHT//2 - 20)
            self.btn_menu.draw(surface)
