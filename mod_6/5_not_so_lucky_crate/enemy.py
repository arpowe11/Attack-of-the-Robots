import pygame
import toolbox
import math
from explosion import Explosion


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player) -> None:
        # Make enemy inherit sprite
        pygame.sprite.Sprite.__init__(self, self.containers)  # NOQA

        # Enemy variables
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load("../assets/Enemy_05.png")
        self.image_hurt = pygame.image.load("../assets/EnemyHurt_05.png")
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("../assets/MediumExplosion1.png"))
        self.explosion_images.append(pygame.image.load("../assets/MediumExplosion2.png"))
        self.explosion_images.append(pygame.image.load("../assets/MediumExplosion3.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = 0
        self.speed = 0.9
        self.health = 20
        self.hurt_timer = 0
        self.damage = 1
        self.obstacle_anger = 0
        self.max_anger = 100


    def update(self, projectiles, crates) -> None:
        # Get the angle between the enemy and the player
        self.angle = toolbox.angle_between_points(self.x, self.player.x, self.y, self.player.y)

        # Move the enemy on the screen
        angle_rads = math.radians(self.angle)
        self.x_move = math.cos(angle_rads) * self.speed  # NOQA
        self.y_move = -math.sin(angle_rads) * self.speed  # NOQA

        # Check to see if the enemy is near a crate
        test_rect = self.rect
        new_x = self.x + self.x_move
        new_y = self.y + self.y_move

        test_rect.center = (new_x, self.y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_x = self.x
                self.get_angry(crate)

        test_rect.center = (self.x, new_y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_y = self.y
                self.get_angry(crate)

        self.x = new_x
        self.y = new_y
        self.rect.center = (self.x, self.y)

        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.get_hit(projectile.damage)
                projectile.explode()

        # rotate between robot images if the robot is hit
        if self.hurt_timer <= 0:
            image_to_rotate = self.image
        else:
            image_to_rotate = self.image_hurt
            self.hurt_timer -= 1

        image_to_draw, image_rect = toolbox.get_rotated_image(image_to_rotate, self.rect, self.angle)

        # Draw the sprite to the screen
        self.screen.blit(image_to_draw, image_rect)

    def get_hit(self, damage) -> None:
        if damage:
            self.hurt_timer = 5

        # Knock back when robot gets shot
        self.x -= self.x_move * 7
        self.y -= self.y_move * 7

        self.health -= damage

        if self.health <= 0:
            self.health = 99999  # set high so self.kill() happens once
            Explosion(self.screen, self.x, self.y, self.explosion_images, 5, 0, False)
            self.kill()

    def get_angry(self, crate) -> None:
        self.obstacle_anger += 1
        if self.obstacle_anger >= self.max_anger:
            crate.get_hit(self.damage)
            self.obstacle_anger = 0
