import pygame.draw


class Button:
    button_color = 255, 0, 0
    pressed_color = 255, 255, 0
    bg_color = 80, 80, 80


    def __init__(self, screen, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.screen = screen

    def draw(self):
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        button_rect = pygame.Rect(self.x + 5, self.y + 5, self.width - 5, self.height - 5)
        pygame.draw.rect(self.screen, Button.bg_color, bg_rect)
        pygame.draw.rect(self.screen, Button.button_color, button_rect)



