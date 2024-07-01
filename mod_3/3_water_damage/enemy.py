import pygame
import toolbox
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player) -> None:
        # Make enemy inherit sprite
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Enemy variables
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load("../assets/Enemy_05.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = 0
        self.speed = 0.9
        self.health = 20

    def update(self, projectiles) -> None:
        # Get the angle between the enemy and the player
        self.angle = toolbox.angle_between_points(self.x, self.player.x, self.y, self.player.y)

        # Move the enemy on the screen
        angle_rads = math.radians(self.angle)
        x_move = math.cos(angle_rads) * self.speed
        y_move = -math.sin(angle_rads) * self.speed
        self.x += x_move
        self.y += y_move
        self.rect.center = (self.x, self.y)

        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.get_hit(projectile.damage)
                projectile.explode()

        image_to_draw, image_rect = toolbox.get_rotated_image(self.image, self.rect, self.angle)

        # Draw the sprite to the screen
        self.screen.blit(image_to_draw, image_rect)

    def get_hit(self, damage) -> None:
        self.health -= damage
        if self.health <= 0:
            self.health = 99999  # set high so self.kill() happens once
            self.kill()
