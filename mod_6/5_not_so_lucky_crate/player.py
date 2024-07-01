import pygame
import toolbox
import projectile
from crate import Crate


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, x, y) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)  # NOQA
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load("../assets/Player_03.png")
        self.image_hurt = pygame.image.load("../assets/Player_03hurt.png")
        self.image_defeated = pygame.image.load("../assets/Enemy_01.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 5
        self.angle = 0
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 10
        self.health_max = 30
        self.health = self.health_max
        self.health_bar_width = self.image.get_width()
        self.health_bar_height = 8
        self.health_bar_green = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)
        self.health_bar_red = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)
        self.alive = True
        self.hurt_timer = 0
        self.crate_ammo = 10
        self.crate_cooldown = 0
        self.crate_cooldown_max = 10

    def update(self, enemies) -> None:
        """
        update the screen as the game is played
        :return:
        """
        self.rect.center = (self.x, self.y)

        # Check for collision with enemies
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.get_hit(0)
                self.get_hit(enemy.damage)

        # Cooldown so the water balloons are spaced out on mouse click
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Cooldown so the crates are spaced out on button click
        if self.crate_cooldown > 0:
            self.crate_cooldown -= 1

        if self.alive:
            # Get mouse position so the character can rotate
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.angle = toolbox.angle_between_points(self.x, mouse_x, self.y, mouse_y)

            # Get the images for the player if he is still alive
            if self.hurt_timer > 0:
                image_to_rotate = self.image_hurt
                self.hurt_timer -= 1
            else:
                image_to_rotate = self.image
        else:
            image_to_rotate = self.image_defeated

        image_to_draw, image_rect = toolbox.get_rotated_image(image_to_rotate, self.rect, self.angle)

        self.screen.blit(image_to_draw, image_rect)

        # Move and draw the health bar based on the players health
        self.health_bar_red.x = self.rect.x
        self.health_bar_red.bottom = self.rect.y - 5
        pygame.draw.rect(self.screen, (255, 0, 0), self.health_bar_red)
        self.health_bar_green.topleft = self.health_bar_red.topleft  # NOQA
        health_percentage = self.health / self.health_max
        self.health_bar_green.width = self.health_bar_width * health_percentage

        if self.alive:
            pygame.draw.rect(self.screen, (0, 255, 0), self.health_bar_green)

    def move(self, x_movement, y_movement, crates) -> None:
        if self.alive:
            # test_rect is used to see if there is an obstacle in front of the player
            test_rect = self.rect
            test_rect.x += self.speed * x_movement
            test_rect.y += self.speed * y_movement
            collision = False

            for crate in crates:
                if not crate.just_placed:
                    if test_rect.colliderect(crate.rect):
                        collision = True

            if not collision:
                self.x += self.speed * x_movement
                self.y += self.speed * y_movement

    def shoot(self) -> None:
        if self.shoot_cooldown <= 0 and self.alive:
            self.shoot_cooldown = self.shoot_cooldown_max
            projectile.WaterBalloon(self.screen, self.x, self.y, self.angle)

    def get_hit(self, damage) -> None:
        if self.alive:
            self.hurt_timer = 5
            self.health -= damage

            # Check if player runs out of health
            if self.health <= 0:
                self.health = 0
                self.alive = False

    def place_crate(self) -> None:
        if self.alive and self.crate_ammo > 0 and self.crate_cooldown <= 0:  # NOQA
            Crate(self.screen, self.x, self.y, self)
            self.crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max


