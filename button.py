import pygame.draw


class Button:
    button_color = 255, 0, 0
    pressed_color = 255, 255, 0
    bg_color = 80, 80, 80


    def __init__(self, screen, x, y, width, height, text, text_size, func):
        self.x = x - width / 2
        self.y = y - height / 2
        self.width = width
        self.height = height
        self.text = text

        self.bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_rect = pygame.Rect(self.x + 5, self.y + 5, self.width - 10, self.height - 10)

        self.color = Button.button_color

        pygame.font.init()
        font = pygame.font.SysFont('Arial', text_size)
        self.text_surface = font.render(self.text, True, (0, 0, 0))

        self.text_x = self.x + (self.width - self.text_surface.get_rect().width) / 2
        self.text_y = self.y + (self.height - self.text_surface.get_rect().height) / 2

        self.func = func

        self.screen = screen

    def is_held(self, pos, mouse_pressed):
        if (self.x < pos[0] < self.x + self.width) and (self.y < pos[1] < self.y + self.height) and mouse_pressed:
            self.color = Button.pressed_color
        else:
            self.color = self.button_color


    def is_released(self, pos):
        if (self.x < pos[0] < self.x + self.width) and (self.y < pos[1] < self.y + self.height):
            return self.func()
        return 0


    def draw(self):
        pygame.draw.rect(self.screen, Button.bg_color, self.bg_rect)
        pygame.draw.rect(self.screen, self.color, self.button_rect)
        self.screen.blit(self.text_surface, (self.text_x, self.text_y))









