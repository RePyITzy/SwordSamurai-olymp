from start_screen import StartScreen
from player_choose import ChoosePlayers
from show_controls import ShowControls
from final_screen import FinalScreen

from modules import game_constants
from modules import game_modules
from modules.game_objects import *

import time
import pygame
import os


def spawnEnemy(game_screen, enemy):
    game_constants.enemies = game_constants.enemies + 1
    enemy = enemy(game_screen, game_constants.entities_group)
    enemy.walk_speed = random.randint(1, 2)
    enemy.rect.center = game_modules.generateSpawnPosition()
    enemy.move_target = game_modules.generateMoveTarget()
    enemy.entity_tag = 'enemy'


def spawnVillager(game_screen, villager):
    villager = villager(game_screen, game_constants.entities_group)
    villager.rect.center = game_modules.generateSpawnPosition()
    villager.move_target = game_modules.generateMoveTarget()
    villager.entity_tag = 'villager'


def enableSafeZone(game_screen):
    game_constants.safe_zone = True
    
    pygame.mixer.music.stop()
    pygame.mixer.music.load(game_constants.SAFE_THEME)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    spawnVillager(game_screen, Healer)
    spawnVillager(game_screen, Upgrader)


def generateWave(game_screen):
    for villager in game_constants.entities_group.sprites():
        if villager.entity_tag == 'villager':
            game_constants.entities_group.remove(villager)

    for enemy in range((game_constants.wave + 2 + len(game_constants.players_group.sprites())) * 2):
        spawnEnemy(game_screen, Zombie)


def StartGame(game_screen=None, players=(0, 1, 0)):
    game_screen = pygame.display.set_mode((800, 600)) if not game_screen else game_screen
    game_clock, game_ticks, game_fps = pygame.time.Clock(), 0, 60
    game_is_running, game_constants.new_wave_after = True, 25000

    interface = Interface(game_screen)
    game_constants.entities_group = pygame.sprite.Group()
    game_constants.tiles_group = pygame.sprite.Group()
    game_constants.objects_group = pygame.sprite.Group()
    game_constants.particles_group = pygame.sprite.Group()
    game_constants.players_group = pygame.sprite.Group()
    game_constants.interface_group = pygame.sprite.Group()

    game_constants.wave, game_constants.enemies = 1, 0

    for index, player in enumerate(players):
        if player == -1: continue 
        controls, player = game_constants.CONTROLS[index], game_constants.PLAYERS[player]
        p = Player(game_screen, player, controls, game_constants.players_group, game_constants.entities_group)

    def draw_by_layered(group):
        sorted_group = sorted(group.sprites(), key=lambda e: (e.health > 0, e.rect.bottom))
        group.empty()
        group.add(sorted_group)
        group.draw(game_screen)

    enableSafeZone(game_screen)
    game_constants.new_wave_after = 2000

    while game_is_running:
        everybody_died = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_modules.terminate('Игра была завершена пользователем')
            
            for player in game_constants.players_group.sprites():
                player.handle_controls(event)

        if game_constants.enemies <= 0 and not game_constants.safe_zone:
            enableSafeZone(game_screen)
            game_constants.wave += 1

        if game_constants.safe_zone:
            game_constants.new_wave_after -= 1

        if game_constants.new_wave_after <= 0:
            game_constants.safe_zone = False
            game_constants.new_wave_after = 2000
            generateWave(game_screen)

        if not game_constants.safe_zone:
            for player in game_constants.players_group.sprites():
                if player.health > 0:
                    everybody_died = False
        else:
            everybody_died = False

        if everybody_died: return game_screen

        game_screen.fill('black')

        draw_by_layered(game_constants.entities_group)
        game_constants.entities_group.update()
        interface.display()

        pygame.display.flip()
        game_clock.tick(game_fps)
        game_ticks += 1


if __name__ == '__main__':
    pygame.init()

    time.sleep(4)
    game_screen = StartScreen()
    players, game_screen = ChoosePlayers(game_screen)
    game_screen = ShowControls(game_screen)
    game_screen = StartGame(game_screen, players)
    FinalScreen(game_screen)
