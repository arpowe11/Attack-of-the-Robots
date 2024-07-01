# Attack of the Robots!!!
#
# Author: Alexander Powell
#

import pygame
import time
from player import Player
from projectile import WaterBalloon
from enemy import Enemy


# Initialize the game variables
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

# load the background image for the game
background_image = pygame.image.load("../assets/BG_Sand.png")

# make all the sprite groups
player_group = pygame.sprite.Group()
projectiles_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

# put every sprite class container in a group
Player.containers = player_group
WaterBalloon.containers = projectiles_group
Enemy.containers = enemies_group

# create class instances
mr_player: Player = Player(screen, game_width/2, game_height/2)
Enemy(screen, 100, 100, mr_player)
Enemy(screen, 100, 500, mr_player)


# ************ Loop Land Below ************
# infinite loop that will only stop once we tell the loop to break
while running:
    # makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # move the player with WASD
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        mr_player.move(1, 0)
    if keys[pygame.K_a]:
        mr_player.move(-1, 0)
    if keys[pygame.K_w]:
        mr_player.move(0, -1)
    if keys[pygame.K_s]:
        mr_player.move(0, 1)
    if pygame.mouse.get_pressed()[0]:
        mr_player.shoot()

    screen.blit(background_image, (0, 0))
    mr_player.update()

    for projectile in projectiles_group:
        projectile.update()

    for enemy in enemies_group:
        enemy.update(projectiles_group)


    # tell pygame to update the screen
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("ATTACK OF THE ROBOTS fps: " + str(clock.get_fps()))
