from os import path
from settings import *
import pygame.mixer


snd_dir = path.join(path.dirname(__file__), 'snd')
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'shield_sound.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'power_sound.wav'))
death_flash = pygame.mixer.Sound(path.join(snd_dir, 'DeathFlash.wav'))
player_explosion = pygame.mixer.Sound(path.join(snd_dir, 'player_explosion.wav'))

expl_sounds = []
for snd in ['Explosion.wav', 'Explosion2.wav', 'Explosion3.wav', 'Explosion4.wav', 'Explosion5.wav', 'Explosion6.wav',
            'Explosion7.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

pygame.mixer.music.load(path.join(snd_dir, 'DST-RailJet-LongSeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)