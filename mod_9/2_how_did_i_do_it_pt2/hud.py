import pygame


class HUD(object):
    def __init__(self, screen, player) -> None:
        self.screen = screen
        self.player = player

        self.state = "ingame"  # NOQA
        self.hud_font = pygame.font.SysFont("skia", 30)
        self.score_text = self.hud_font.render("", True, (255, 255, 255))

    def update(self) -> None:
        self.score_text = self.hud_font.render("Score: " + str(self.player.score), True, (255, 255, 255))
        self.screen.blit(self.score_text, (10, 10))






