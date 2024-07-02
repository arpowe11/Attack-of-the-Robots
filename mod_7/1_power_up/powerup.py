import pygame
import random
import toolbox


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screen, x, y) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)  # NOQA

        # Set up PowerUp variables
        self.screen = screen
        self.x = x
        self.y = y
        self.pick_power = random.randint(0, 0)

        if self.pick_power == 0:  # Crate ammo
            self.image = pygame.image.load("../assets/powerupCrate.png")
            self.background_image = pygame.image.load("../assets/powerupBackgroundBlue.png")
            self.power_type = "crateammo"  # NOQA

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.background_angle = 0
        self.spinny_speed = 2

    def update(self) -> None:
        self.background_angle += self.spinny_speed
        bg_image_to_draw, bg_rect = toolbox.get_rotated_image(self.background_image, self.rect, self.background_angle)

        self.screen.blit(bg_image_to_draw, bg_rect)
        self.screen.blit(self.image, self.rect)
