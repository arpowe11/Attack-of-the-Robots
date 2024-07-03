import pygame


class HUD(object):
    def __init__(self, screen, player) -> None:
        self.screen = screen
        self.player = player

        self.state = "ingame"
        self.hud_font = pygame.font.SysFont("default", 30)
        self.score_text = self.hud_font.render("Beep Boop", True, (255, 255, 255))

    def update(self) -> None:
        self.screen.blit(self.score_text, (10, 10))






