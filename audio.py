import pygame
import math
import wave
import struct
import os

def generate_wav(filename, frequency=440, duration=0.1, volume=0.5, wave_type='sine'):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            if wave_type == 'sine':
                value = math.sin(2.0 * math.pi * frequency * t)
            elif wave_type == 'square':
                value = 1.0 if math.sin(2.0 * math.pi * frequency * t) > 0 else -1.0
            elif wave_type == 'noise':
                import random
                value = random.uniform(-1.0, 1.0)
            else:
                value = 0.0
            
            # Envelope (fade out)
            envelope = 1.0 - (i / num_samples)
            value *= volume * envelope
            
            packed_value = struct.pack('h', int(value * 32767.0))
            f.writeframes(packed_value)

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.generate_sounds()

    def generate_sounds(self):
        os.makedirs("assets", exist_ok=True)
        if not os.path.exists("assets/click.wav"):
            generate_wav("assets/click.wav", frequency=800, duration=0.1, volume=0.3, wave_type='sine')
        if not os.path.exists("assets/thunder.wav"):
            generate_wav("assets/thunder.wav", frequency=100, duration=1.5, volume=0.8, wave_type='noise')
        if not os.path.exists("assets/win.wav"):
            generate_wav("assets/win.wav", frequency=600, duration=1.0, volume=0.5, wave_type='sine')
        if not os.path.exists("assets/loss.wav"):
            generate_wav("assets/loss.wav", frequency=150, duration=1.5, volume=0.6, wave_type='square')

        self.sounds['click'] = pygame.mixer.Sound("assets/click.wav")
        self.sounds['thunder'] = pygame.mixer.Sound("assets/thunder.wav")
        self.sounds['win'] = pygame.mixer.Sound("assets/win.wav")
        self.sounds['loss'] = pygame.mixer.Sound("assets/loss.wav")

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
