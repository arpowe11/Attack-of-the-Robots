import pygame
import toolbox
import projectile
from crate import Crate
from crate import ExplosiveCrate


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
        self.explosive_crate_ammo = 5
        self.crate_cooldown = 0
        self.crate_cooldown_max = 10
        self.shot_type = "normal"
        self.special_ammo = 0
        self.score = 0
        self.sfx_shot = pygame.mixer.Sound("../assets/sfx/shot.wav")
        self.sfx_place = pygame.mixer.Sound("../assets/sfx/bump.wav")
        self.sfx_defeat = pygame.mixer.Sound("../assets/sfx/electrocute.wav")

    def update(self, enemies, explosions) -> None:
        """
        update the screen as the game is played
        :return:
        """

        self.rect.center = (self.x, self.y)

        # Check for collisions with enemies
        for explosion in explosions:
            if explosion.damage and explosion.damage_player:
                if self.rect.colliderect(explosion.rect):
                    self.get_hit(explosion.damage)

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

        # Check if the player is going off the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
        self.x = self.rect.centerx
        self.y = self.rect.centery


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
            self.sfx_shot.play()
            if self.shot_type == "normal":
                projectile.WaterBalloon(self.screen, self.x, self.y, self.angle)
            elif self.shot_type == "split":
                projectile.SplitWaterBalloon(self.screen, self.x, self.y, self.angle - 15)
                projectile.SplitWaterBalloon(self.screen, self.x, self.y, self.angle)
                projectile.SplitWaterBalloon(self.screen, self.x, self.y, self.angle + 15)
                self.special_ammo -= 1
            elif self.shot_type == "stream":
                projectile.WaterDroplet(self.screen, self.x, self.y, self.angle)
                self.special_ammo -= 1
            elif self.shot_type == "burst":
                projectile.ExplosiveWaterBalloon(self.screen, self.x, self.y, self.angle)
                self.special_ammo -= 1


            self.shoot_cooldown = self.shoot_cooldown_max

            if self.special_ammo <= 0:
                self.power_up("normal")

    def get_hit(self, damage) -> None:
        if self.alive:
            self.hurt_timer = 5
            self.health -= damage

            # Check if player runs out of health
            if self.health <= 0:
                self.sfx_defeat.play()
                self.health = 0
                self.alive = False

    def place_crate(self) -> None:
        if self.alive and self.crate_ammo > 0 and self.crate_cooldown <= 0:  # NOQA
            Crate(self.screen, self.x, self.y, self)
            self.crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max
            self.sfx_place.play()

    def place_explosive_crate(self) -> None:
        if self.alive and self.explosive_crate_ammo > 0 and self.crate_cooldown <= 0:  # NOQA
            ExplosiveCrate(self.screen, self.x, self.y, self)
            self.explosive_crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max
            self.sfx_place.play()

    def power_up(self, power_type) -> None:
        if power_type == "crateammo":  # NOQA
            self.crate_ammo += 10
            self.get_score(10)
        elif power_type == "explosiveammo":  # NOQA
            self.explosive_crate_ammo += 5
            self.get_score(10)
        elif power_type == "split":
            self.shot_type = "split"
            self.special_ammo = 40
            self.shoot_cooldown_max = 20
            self.get_score(20)
        elif power_type == "normal":
            self.shot_type = "normal"
            self.shoot_cooldown_max = 10
        elif power_type == "stream":
            self.shot_type = "stream"
            self.special_ammo = 300
            self.shoot_cooldown_max = 3
            self.get_score(20)
        elif power_type == "burst":
            self.shot_type = "burst"
            self.special_ammo = 35
            self.shoot_cooldown_max = 30
            self.get_score(20)

    def get_score(self, score) -> None:
        if self.alive:
            self.score += score

