import pygame
import random
from settings import *

pygame.init()  # команда для запуска pygame
pygame.mixer.init() # Загрузка мелодий
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ШВЕПС!")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('verdana') # СЧЕТ

import graphic
import sound
import explosion
import mob
import pow_b
import bullet
import player_b

# ---------------Создание игры и окна-------------


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)  # рендер текста
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# ---------Метеоры-------------------


def newmob():
    m = mob.Mob()
    all_sprites.add(m)
    MOBS.add(m)  # МДА


# Здоровье


def health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


# Отображение счетчика жизней


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


# Интерфейс
def show_go_screen():
    screen.blit(graphic.background, graphic.background_rect)
    draw_text(screen, 'ШВЕЕПС!', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, 'СТРЕЛКИ ДЛЯ ПЕРЕДВИЖЕНИЯ, ПРОБЕЛ ДЛЯ СТРЕЛЬБЫ!', 16, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "НАЖМИ, ЧТОБЫ НАЧАТЬ СНОВА!", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# ----------Каждый созданный спрайт добавляем в группу all_sprites---------------
all_sprites = pygame.sprite.Group()
MOBS = pygame.sprite.Group()
bullets = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
player = player_b.Player()
all_sprites.add(player)
for i in range(8):
    newmob()

score = 0
pygame.mixer.music.play(loops=-1)  # бесконечно возпроизводится

# ----------Цикл игры----------------------------------------
game_over = False
running = True

while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        power_ups = pygame.sprite.Group()
        player = player_b.Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
    clock.tick(FPS)
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_SPACE]:
        player.shoot(all_sprites, bullets)
    # Держим цикл на правильной скорости
    for event in pygame.event.get():  # Ввод процесса (события)
        if event.type == pygame.QUIT:  # чек если закрыто окно
            running = False

    # ---------Обновление--------------------------------------------------------------
    all_sprites.update()

    # ______Проверка, не ударил ли моб игрока_________
    hits = pygame.sprite.groupcollide(MOBS, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius  # высчитывает радиус от 50 и получаем score
        random.choice(sound.expl_sounds).play()
        expl = explosion.Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = pow_b.Pow(hit.rect.center)
            all_sprites.add(pow)
            power_ups.add(pow)
        newmob()

    # *******-ПРОВЕРКА СТОЛКНОВЕНИЙ ИГРОКА И УЛУЧШЕНИЯ-******
    hits = pygame.sprite.spritecollide(player, power_ups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            sound.shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
                sound.shield_sound.play()
        if hit.type == 'gun':
            player.powerup()

    # spritecollide - сравнивается только один с группой
    hits = pygame.sprite.spritecollide(player, MOBS, True,
                                       pygame.sprite.collide_circle)  # (спрайт, группа сравнения, параметр столкновения)
    # if hits: # if hits = true то running false и конец игры
    #     running = False
    for hit in hits:
        player.shield -= hit.radius * 2  # в зависимости от радиуса получаем урон (чем больше радиус - тем больше урон)
        sound.player_explosion.play()
        expl = explosion.Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = explosion.Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            sound.death_flash.play()
            player.shield = 100

        # Если игрок умер - игра будет окончена
        if player.lives == 0 and not death_explosion.alive():
            game_over = True

    # ---------Рендеринг---------------------------------------------------------------
    screen.fill(BLACK)
    screen.blit(graphic.background, graphic.background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    health(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, graphic.player_mini_img)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
