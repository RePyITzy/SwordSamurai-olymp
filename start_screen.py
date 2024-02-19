import pygame
import random
import os, sys


def StartScreen():
    MUSIC_PATH = 'resources\\music\\loading-theme.mp3'
    SCREEN_PATH = 'resources\\assets\\loading-screen.png'
    FINISH_PATH = 'resources\\assets\\loaded-screen.png'

    pygame.display.set_caption('Sword Samurai')
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()

    startscreen = pygame.sprite.Sprite(all_sprites)
    startscreen_alpha = 0

    startscreen.image = pygame.image.load(SCREEN_PATH)
    startscreen.image.set_alpha(startscreen_alpha)
    startscreen.rect = startscreen.image.get_rect()

    screen_fps, ticks = 80, 1
    loaded, about_finish = False, False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYUP and loaded: about_finish = True
            if event.type == pygame.MOUSEBUTTONUP and loaded: about_finish = True

        if ticks % 2 == 0 and not about_finish:
            startscreen_alpha += 1
            startscreen.image.set_alpha(startscreen_alpha)
        
        if startscreen_alpha > random.randint(50, 100):
            startscreen.image = pygame.image.load(FINISH_PATH)
            startscreen.image.set_alpha(startscreen_alpha)
            loaded = True
        
        if ticks % 2 == 0 and about_finish:
             if startscreen_alpha > 255: startscreen_alpha = 255
             startscreen_alpha -= 2
             pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.0002567)
             startscreen.image.set_alpha(startscreen_alpha)

             if startscreen_alpha < -50: break
            
        screen.fill('black')
        all_sprites.draw(screen)

        clock.tick(screen_fps)
        pygame.display.flip()
        ticks += 1
    
    screen.fill('black')
    return screen


if __name__ == '__main__':
    pygame.init()
    StartScreen()
