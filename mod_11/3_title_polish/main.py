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
from crate import ExplosiveCrate
from explosion import Explosion
from powerup import PowerUp
from hud import HUD


# Initialize the game variables
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True
game_started = False

# Load the background image for the game
background_image = pygame.image.load("../assets/BG_Urban.png")

# Make all the sprite groups
player_group = pygame.sprite.Group()
projectiles_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
crate_group = pygame.sprite.Group()
explosions_group = pygame.sprite.Group()
powerups_group = pygame.sprite.Group()

# Put every sprite class container in a group
Player.containers = player_group
WaterBalloon.containers = projectiles_group
Enemy.containers = enemies_group
Crate.containers = crate_group
Explosion.containers = explosions_group
PowerUp.containers = powerups_group

# Enemy spawn frames/timer
enemy_spawn_timer_max = 100
enemy_spawn_timer = 0
enemy_spawn_speedup_timer_max = 400  # after 400 frames, enemies spawn faster
enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max

# Create class instances
mr_player: Player = Player(screen, game_width/2, game_height/2)
hud: HUD = HUD(screen, mr_player)


def start_game():
    """
    Start game function makes the game switch from
    main menu to in-game

    :return:
    """

    global game_started
    global hud
    global mr_player
    global enemy_spawn_timer_max
    global enemy_spawn_timer
    global enemy_spawn_speedup_timer

    enemy_spawn_timer_max = 100
    enemy_spawn_timer = 0
    enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max

    game_started = True
    hud.state = "ingame"  # NOQA
    mr_player.__init__(screen, game_width/2, game_height/2)

    # Make a bunch of crates
    for i in range(0, 10):
        ExplosiveCrate(screen, random.randint(0, game_width), random.randint(0, game_height), mr_player)
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

    screen.blit(background_image, (0, 0))  # draw the background image

    if not game_started:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                start_game()
                break


    if game_started:
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
        if pygame.mouse.get_pressed()[2] or keys[pygame.K_f]:
            mr_player.place_explosive_crate()

        # Gradually speed up Enemy spawning
        enemy_spawn_speedup_timer -= 1
        if enemy_spawn_speedup_timer <= 0:
            if enemy_spawn_timer_max > 20:
                enemy_spawn_timer_max -= 10
            enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max

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


        for powerup in powerups_group:
            powerup.update(mr_player)

        for explosion in explosions_group:
            explosion.update()

        for enemy in enemies_group:
            enemy.update(projectiles_group, crate_group, explosions_group)

        for projectile in projectiles_group:
            projectile.update()

        for crate in crate_group:
            crate.update(projectiles_group, explosions_group)

        mr_player.update(enemies_group, explosions_group)


    if not mr_player.alive:
        if hud.state == "ingame":  # NOQA
            hud.state = "gameover"  # NOQA
        elif hud.state == "mainmenu":  # NOQA
            game_started = False
            player_group.empty()
            projectiles_group.empty()
            enemies_group.empty()
            powerups_group.empty()
            explosions_group.empty()
            crate_group.empty()

    hud.update()

    # tell pygame to update the screen
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("ATTACK OF THE ROBOTS fps: " + str(clock.get_fps()))
