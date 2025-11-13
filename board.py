import pygame
from sudoku_generator import generate_sudoku

class Board:
    def __init__(self, size, difficulty):
        self.screen = pygame.display.set_mode((size + 2, size + size / 9))
        pygame.display.set_caption("Sudoku")
        self.size = size
        self.square_size = size / 9
        self.current_cell = None

        self.nums = generate_sudoku(9, difficulty)

    def draw_grid(self):
        for x in range(2):
            for num in range(10):
                if num % 3 == 0:
                    width = 4
                else:
                    width = 1
                if x == 0:
                    pygame.draw.line(self.screen, (0, 0, 0), (0, num * self.square_size), (self.size + 2, num * self.square_size), width)
                else:
                    pygame.draw.line(self.screen, (0, 0, 0), (num * self.square_size, 0), (num * self.square_size, self.size), width)

    def highlight_cell(self):
        if self.current_cell is not None:
            rect = pygame.Rect(self.current_cell[0] * self.square_size, self.current_cell[1] * self.square_size, self.square_size + 2, self.square_size + 2)
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 4)

    def highlight_affected(self):
        if self.current_cell is not None:
            hori_rect = pygame.Rect(0, self.current_cell[1] * self.square_size, self.size, self.square_size + 1)
            vert_rect = pygame.Rect(self.current_cell[0] * self.square_size + 1, 0, self.square_size, self.size)
            pygame.draw.rect(self.screen, (180, 180, 180), hori_rect)
            pygame.draw.rect(self.screen, (180, 180, 180), vert_rect)


    def click(self):
        pos = pygame.mouse.get_pos()
        cell = (pos[0] // self.square_size, pos[1] // self.square_size)
        if cell == self.current_cell:
            self.current_cell = None
        else:
            self.current_cell = cell


    def update(self):
        self.screen.fill((255, 255, 255))
        self.highlight_affected()
        self.draw_grid()
        self.highlight_cell()

        pygame.display.flip()



