import pygame.sprite
from settings import *
from bullet import Bullet
import sound
import graphic


class Player(pygame.sprite.Sprite):  # инициализатор встроенных классов спрайт
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphic.pygame.transform.scale(graphic.player_img,
                                            (90, 78))  # pygame.Surface((50, 40)) # определяем свойство image
        # self.image.fill(GREEN)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()  # определяем rectangle спрайта
        self.radius = 26
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) Красные кружки
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):  # перемещает спрайт с конкретной скоростью
        # *******-ПОКАЗЫВАЕТ ИГРОКА ПОСЛЕ ПОТЕРИ ЖИЗНИ СПУСТЯ 1 СЕК-*******
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        # *******-СПРАЙТ НЕ ПРОПАДАЕТ ЗА ПРЕДЕЛЫ ЭКРАНА-********
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        # тайм-аут для бонусов
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

    def shoot(self, all_sprites, bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                sound.shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                sound.shoot_sound.play()

    # ********-СКРЫВАЕМ-ИГРОКА-***********
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        sound.power_sound.play()