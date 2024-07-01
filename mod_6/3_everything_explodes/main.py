# Attack of the Robots!!!
#
# Author: Alexander Powell
#

import pygame
import random
from player import Player
from projectile import WaterBalloon
from enemy import Enemy
from crate import Crate
from explosion import Explosion


# Initialize the game variables
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

# Load the background image for the game
background_image = pygame.image.load("../assets/BG_Sand.png")

# Make all the sprite groups
player_group = pygame.sprite.Group()
projectiles_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
crate_group = pygame.sprite.Group()
explosions_group = pygame.sprite.Group()

# Put every sprite class container in a group
Player.containers = player_group
WaterBalloon.containers = projectiles_group
Enemy.containers = enemies_group
Crate.containers = crate_group
Explosion.containers = explosions_group

enemy_spawn_timer_max = 80
enemy_spawn_timer = 0

# Create class instances
mr_player: Player = Player(screen, game_width/2, game_height/2)

# Spawn 10 crates
for i in range(0, 10):
    Crate(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)


# ************ Loop Land Below ************
# infinite loop that will only stop once we tell the loop to break
while running:
    # makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # move the player with WASD, shoot, and place crates
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        mr_player.move(1, 0, crate_group)
    if keys[pygame.K_a]:
        mr_player.move(-1, 0, crate_group)
    if keys[pygame.K_w]:
        mr_player.move(0, -1, crate_group)
    if keys[pygame.K_s]:
        mr_player.move(0, 1, crate_group)
    if pygame.mouse.get_pressed()[0]:
        mr_player.shoot()
    if keys[pygame.K_SPACE]:
        mr_player.place_crate()

    # Make Enemy spawning happen
    enemy_spawn_timer -= 1
    if enemy_spawn_timer <= 0:
        new_enemy = Enemy(screen, 0, 0, mr_player)
        side_to_spawn = random.randint(0, 3)  # 0=top, 1=bottom, 2=left, 3=right
        if side_to_spawn == 0:
            new_enemy.x = random.randint(0, game_width)
            new_enemy.y = -new_enemy.image.get_height()
        elif side_to_spawn == 1:
            new_enemy.x = random.randint(0, game_width)
            new_enemy.y = game_height + new_enemy.image.get_height()
        elif side_to_spawn == 2:
            new_enemy.x = -new_enemy.image.get_width()
            new_enemy.y = random.randint(0, game_height)
        elif side_to_spawn == 3:
            new_enemy.x = game_height + new_enemy.image.get_width()
            new_enemy.y = random.randint(0, game_height)
        enemy_spawn_timer = enemy_spawn_timer_max

    screen.blit(background_image, (0, 0))  # draw the background image

    for enemy in enemies_group:
        enemy.update(projectiles_group, crate_group)

    for projectile in projectiles_group:
        projectile.update()

    for crate in crate_group:
        crate.update(projectiles_group)

    for explosion in explosions_group:
        explosion.update()

    mr_player.update(enemies_group)

    # tell pygame to update the screen
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("ATTACK OF THE ROBOTS fps: " + str(clock.get_fps()))
