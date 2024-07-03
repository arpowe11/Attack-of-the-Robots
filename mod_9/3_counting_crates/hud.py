import pygame


class HUD(object):
    def __init__(self, screen, player) -> None:
        self.screen = screen
        self.player = player

        self.state = "ingame"  # NOQA
        self.hud_font = pygame.font.SysFont("skia", 30)
        self.score_text = self.hud_font.render("", True, (255, 255, 255))

        # Load the icon images for the tiles
        self.crate_icon = pygame.image.load("../assets/Crate.png")
        self.explosive_crate_icon = pygame.image.load("../assets/ExplosiveBarrel.png")

        # Make the ammo tiles
        self.crate_ammo_tile = AmmoTile(self.screen, self.crate_icon, self.hud_font)
        self.explosive_crate_ammo_tile = AmmoTile(self.screen, self.explosive_crate_icon, self.hud_font)

    def update(self) -> None:
        # Draw the score text
        self.score_text = self.hud_font.render("Score: " + str(self.player.score), True, (255, 255, 255))
        self.screen.blit(self.score_text, (10, 10))

        # Draw the ammo tiles
        self.crate_ammo_tile.update(50, self.screen.get_height(), self.player.crate_ammo)
        self.explosive_crate_ammo_tile.update(250, self.screen.get_height(), self.player.explosive_crate_ammo)


class AmmoTile(object):
    def __init__(self, screen, icon, font) -> None:
        self.screen = screen
        self.icon = icon
        self.font = font
        self.bg_image = pygame.image.load("../assets/hudTile.png")


    def update(self, x, y, ammo) -> None:
        # Draw tile background
        tile_rect = self.bg_image.get_rect()
        tile_rect.bottomleft = (x, y)  # NOQA
        self.screen.blit(self.bg_image, tile_rect)

        # Draw icon
        icon_rect = self.icon.get_rect()
        icon_rect.center = tile_rect.center
        self.screen.blit(self.icon, icon_rect)

        # Draw ammo number/amount
        ammo_text = self.font.render(str(ammo), True, (255, 255, 255))
        self.screen.blit(ammo_text, tile_rect.topleft)







