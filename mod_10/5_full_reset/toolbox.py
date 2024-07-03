import pygame
import math


def get_rotated_image(image, rect, angle) -> tuple:
    """
    rotates the image on screen and creates a new rectangle
    for each rotation

    :param image:
    :param rect:
    :param angle:
    :return tuple:
    """

    new_image = pygame.transform.rotate(image, angle)
    new_rect = new_image.get_rect(center=rect.center)

    return new_image, new_rect


def angle_between_points(x1, x2, y1, y2) -> float:
    """
    calculates the angle between the mouse and the player

    :param x1:
    :param x2:
    :param y1:
    :param y2:
    :return float:
    """

    x_difference = x2 - x1
    y_difference = y2 - y1
    angle = math.degrees(math.atan2(-y_difference, x_difference))

    return angle


def centering_chords(thingy, screen) -> tuple[float, float]:
    """
    Returns the coordinates that will put thingy in the center of the screen

    :param thingy:
    :param screen:
    :return:
    """

    new_x = screen.get_width() / 2 - thingy.get_width() / 2
    new_y = screen.get_height() / 2 - thingy.get_height() / 2

    return new_x, new_y




