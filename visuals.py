import pygame
import random
from settings import *

class Particle:
    def __init__(self, x, y, size, life, color, velocity):
        self.x = x
        self.y = y
        self.size = size
        self.life = life
        self.max_life = life
        self.color = color
        self.velocity = velocity

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def update(self, dt):
        for p in reversed(self.particles):
            p.x += p.velocity[0] * dt
            p.y += p.velocity[1] * dt
            p.life -= dt
            if p.life <= 0:
                self.particles.remove(p)

    def draw(self, surface):
        pass

class FogSystem(ParticleSystem):
    def update(self, dt):
        super().update(dt)
        if len(self.particles) < FOG_DENSITY:
            self.particles.append(Particle(
                x=random.randint(-200, WIDTH + 200),
                y=random.randint(HEIGHT//2, HEIGHT),
                size=random.randint(50, 200),
                life=random.uniform(5, 15),
                color=(50, 50, 60, random.randint(10, 40)),
                velocity=(random.uniform(10, 30), random.uniform(-5, 5))
            ))

    def draw(self, surface):
        for p in self.particles:
            alpha = int(255 * (p.life / p.max_life))
            color = (*p.color[:3], min(p.color[3], alpha))
            surf = pygame.Surface((p.size*2, p.size*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (p.size, p.size), p.size)
            surface.blit(surf, (int(p.x - p.size), int(p.y - p.size)))

class RainSystem(ParticleSystem):
    def update(self, dt):
        super().update(dt)
        while len(self.particles) < RAIN_DROPS:
            self.particles.append(Particle(
                x=random.randint(-100, WIDTH + 100),
                y=random.randint(-500, -50),
                size=random.randint(1, 3),
                life=random.uniform(1, 3),
                color=(150, 150, 180, 200),
                velocity=(random.uniform(50, 100), random.uniform(500, 800))
            ))

    def draw(self, surface):
        for p in self.particles:
            pygame.draw.line(surface, p.color, (int(p.x), int(p.y)), (int(p.x - p.velocity[0]*0.05), int(p.y - p.velocity[1]*0.05)), p.size)

class SceneRenderer:
    def __init__(self):
        self.fog = FogSystem()
        self.rain = RainSystem()
        self.shake_offset = [0, 0]
        self.shake_duration = 0
        self.shake_intensity = 0
        self.thunder_flash = 0

    def trigger_shake(self, intensity, duration):
        self.shake_intensity = intensity
        self.shake_duration = duration

    def trigger_thunder(self):
        self.thunder_flash = 1.0
        self.trigger_shake(10, 0.5)

    def update(self, dt):
        self.fog.update(dt)
        self.rain.update(dt)

        if self.shake_duration > 0:
            self.shake_duration -= dt
            self.shake_offset = [random.randint(-self.shake_intensity, self.shake_intensity),
                                 random.randint(-self.shake_intensity, self.shake_intensity)]
        else:
            self.shake_offset = [0, 0]

        if self.thunder_flash > 0:
            self.thunder_flash -= dt * 2

    def draw_gallows(self, surface, mistakes):
        # Base platform
        pygame.draw.rect(surface, (40, 30, 25), (WIDTH//2 - 200, HEIGHT - 150, 400, 50))
        # Main pillar
        pygame.draw.rect(surface, (30, 20, 15), (WIDTH//2 - 150, 150, 30, HEIGHT - 300))
        # Top beam
        pygame.draw.rect(surface, (30, 20, 15), (WIDTH//2 - 150, 150, 200, 30))
        # Support beam
        pygame.draw.line(surface, (30, 20, 15), (WIDTH//2 - 120, 180), (WIDTH//2 - 150, 210), 10)
        # Rope
        pygame.draw.rect(surface, (150, 130, 100), (WIDTH//2 + 30, 180, 5, 80))

        # Body parts based on mistakes
        center_x = WIDTH//2 + 32
        center_y = 260
        if mistakes > 0:
            # Head
            pygame.draw.circle(surface, (180, 160, 140), (center_x, center_y + 20), 20)
        if mistakes > 1:
            # Body
            pygame.draw.line(surface, (100, 80, 80), (center_x, center_y + 40), (center_x, center_y + 120), 15)
        if mistakes > 2:
            # Left Arm
            pygame.draw.line(surface, (100, 80, 80), (center_x, center_y + 50), (center_x - 40, center_y + 100), 10)
        if mistakes > 3:
            # Right Arm
            pygame.draw.line(surface, (100, 80, 80), (center_x, center_y + 50), (center_x + 40, center_y + 100), 10)
        if mistakes > 4:
            # Left Leg
            pygame.draw.line(surface, (80, 60, 60), (center_x, center_y + 120), (center_x - 30, center_y + 200), 12)
        if mistakes > 5:
            # Right Leg
            pygame.draw.line(surface, (80, 60, 60), (center_x, center_y + 120), (center_x + 30, center_y + 200), 12)

    def draw(self, surface, mistakes):
        # Base background
        surface.fill(BG_COLOR)

        # Thunder flash
        if self.thunder_flash > 0:
            flash_surf = pygame.Surface((WIDTH, HEIGHT))
            flash_surf.fill((200, 200, 220))
            flash_surf.set_alpha(int(self.thunder_flash * 100))
            surface.blit(flash_surf, (0, 0))

        main_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # Draw gallows
        self.draw_gallows(main_surf, mistakes)

        self.fog.draw(main_surf)
        self.rain.draw(main_surf)

        # Apply screen shake
        surface.blit(main_surf, self.shake_offset)
