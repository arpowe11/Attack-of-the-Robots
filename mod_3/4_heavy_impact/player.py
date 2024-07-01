import pygame
import toolbox
import projectile


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load("../assets/Player_03.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 5
        self.angle = 0
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 10

    def update(self) -> None:
        """
        update the screen as the game is played
        :return:
        """
        self.rect.center = (self.x, self.y)

        # Cooldown so the water balloons are spaced out on mouse click
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = toolbox.angle_between_points(self.x, mouse_x, self.y, mouse_y)

        image_to_draw, image_rect = toolbox.get_rotated_image(self.image, self.rect, self.angle)
        self.screen.blit(image_to_draw, image_rect)

    def move(self, x_movement, y_movement) -> None:
        self.x += self.speed * x_movement
        self.y += self.speed * y_movement

    def shoot(self) -> None:
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.shoot_cooldown_max
            projectile.WaterBalloon(self.screen, self.x, self.y, self.angle)
