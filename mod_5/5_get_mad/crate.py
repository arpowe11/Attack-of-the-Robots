import pygame


class Crate(pygame.sprite.Sprite):
    def __init__(self, screen, x, y) -> None:
        """ Make enemy inherit sprite """
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Set up crate variables
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load("../assets/Crate.png")
        self.image_hurt = pygame.image.load("../assets/Crate_hurt.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.health = 50
        self.hurt_timer = 0

    def update(self, projectiles) -> None:
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                projectile.explode()
                self.get_hit(projectile.damage)

        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            image_to_draw = self.image_hurt
        else:
            image_to_draw = self.image

        self.screen.blit(image_to_draw, self.rect)

    def get_hit(self, damage) -> None:
        self.health -= damage
        self.hurt_timer = 5

        if self.health <= 0:
            self.health = 99999
            self.kill()







