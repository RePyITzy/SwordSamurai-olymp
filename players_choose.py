from modules.game_constants import *
import pygame

def ChoosePlayers(screen):
    SCREEN = 'resources\\assets\\select_players.png'
    
    SAMURAI = 'resources\\assets\\photo-samurai.png'
    COMMANDER = 'resources\\assets\\photo-commander.png'
    ARCHER = 'resources\\assets\\photo-archer.png'

    c_start_button = [(281, 539), (523, 572)]
    c_player_1 = [(65, 136), (230, 435)]
    c_player_2 = [(316, 132), (489, 435)]
    c_player_3 = [(568, 136), (731, 435)]

    player_1_hero, player_2_hero, player_3_hero = [-1] * 3
    heros = ['Samurai', 'Archer', 'Commander']
    images = [SAMURAI, ARCHER, COMMANDER]

    pygame.mixer.music.load(WAITING_THEME)
    pygame.mixer.music.set_volume(15)
    pygame.mixer.music.play(-1)

    player_selected_sound = pygame.mixer.Sound(SOUND_SELECT)
    player_select_done = pygame.mixer.Sound(SOUND_STOP)
    player_dont_selected = pygame.mixer.Sound(SOUND_ERROR)

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    selectscreen = pygame.sprite.Sprite(all_sprites)
    selectscreen.image = pygame.image.load(SCREEN)
    selectscreen.rect = selectscreen.image.get_rect()

    select_running, move_screen = True, False
    screen_fps, ticks, offset = 80, 0, 0

    def change_player(obj):
        if obj == len(heros) - 1: return -1
        else: return (obj + 1) % len(heros)

    while select_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            
            if event.type == pygame.KEYUP:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    if all(plr == -1 for plr in [player_1_hero, player_2_hero, player_3_hero]): 
                        player_dont_selected.play()
                    else:
                        pygame.mixer.music.stop()
                        player_select_done.play()
                        move_screen = True

            if event.type == pygame.MOUSEBUTTONUP:
                if move_screen: continue
                x, y = event.pos

                # Если нажали на рамку "WASD"
                if c_player_1[0][0] <= x <= c_player_1[1][0]:
                    if c_player_1[0][1] <= y <= c_player_1[1][1]:
                        player_selected_sound.play()
                        player_1_hero = change_player(player_1_hero)
                
                # Если нажали на рамку "СТРЕЛКИ"
                if c_player_2[0][0] <= x <= c_player_2[1][0]:
                    if c_player_2[0][1] <= y <= c_player_2[1][1]:
                        player_selected_sound.play()
                        player_2_hero = change_player(player_2_hero)

                # Если нажали на рамку "МЫШЬ"
                if c_player_3[0][0] <= x <= c_player_3[1][0]:
                    if c_player_3[0][1] <= y <= c_player_3[1][1]:
                        player_selected_sound.play()
                        player_3_hero = change_player(player_3_hero)

                # Если нажали на кнопку "Начать игру"
                if c_start_button[0][0] <= x <= c_start_button[1][0]:
                    if c_start_button[0][1] <= y <= c_start_button[1][1]:
                        if all(plr == -1 for plr in [player_1_hero, player_2_hero, player_3_hero]): player_dont_selected.play()
                        else:
                            pygame.mixer.music.stop()
                            player_select_done.play()
                            move_screen = True
        
        if move_screen:
            if selectscreen.rect.y > 900: select_running = False
            selectscreen.rect = selectscreen.rect.move(0, 5)
            offset += 5
        
        screen.fill('black')
        all_sprites.draw(screen)

        if not (player_1_hero == -1):
            render = pygame.image.load(images[player_1_hero])
            coords = (c_player_1[0][0], c_player_1[0][1] + offset)
            screen.blit(render, coords)
        
        if not (player_2_hero == -1):
            render = pygame.image.load(images[player_2_hero])
            coords = (c_player_2[0][0], c_player_2[0][1] + offset)
            screen.blit(render, coords)
        
        if not (player_3_hero == -1):
            render = pygame.image.load(images[player_3_hero])
            coords = (c_player_3[0][0], c_player_3[0][1] + offset)
            screen.blit(render, coords)

        clock.tick(screen_fps)
        pygame.display.flip()
        ticks += 1
    
    return (player_1_hero, player_2_hero, player_3_hero), screen


if __name__ == '__main__':
    from start_screen import StartScreen
    
    pygame.init()
    ChoosePlayers(pygame.display.set_mode((800, 600)))
