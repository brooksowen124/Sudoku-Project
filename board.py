import pygame
import copy

from sudoku_generator import generate_sudoku
from button import Button

class Board:
    def __init__(self, size, difficulty):
        self.screen = pygame.display.set_mode((size + 2, size + size * 2 / 9))
        pygame.display.set_caption("Sudoku")
        self.size = size
        self.square_size = size / 9
        self.current_cell = None

        self.nums, self.solved_board = generate_sudoku(9, difficulty)
        self.original = copy.deepcopy(self.nums)

        self.running = True

        self.buttons = {
            "Reset": Button(self.screen, size / 4 * 1, self.size * 10 / 9, self.square_size * 1.6, self.square_size * 0.8, "Reset", 20, self.reset),
            "Restart": Button(self.screen, size / 4 * 2, self.size * 10 / 9, self.square_size * 1.6, self.square_size * 0.8, "Restart", 20, lambda: self.restart(difficulty)),
            "Exit": Button(self.screen, size / 4 * 3, self.size * 10 / 9, self.square_size * 1.6, self.square_size * 0.8, "Exit", 20, self.quit)
        }

        pygame.font.init()


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
            for row in range(9):
                for col in range(9):
                    if self.original[row][col] == 0:
                        color = 255, 255, 255
                    else:
                        color = 210, 210, 210

                    if self.current_cell is not None:

                        if col == self.current_cell[0] or row == self.current_cell[1] or (col - col % 3 <= self.current_cell[0] <= col - col % 3 + 2) and (row - row % 3 <= self.current_cell[1] <= row - row % 3 + 2):
                            if self.original[row][col] == 0:
                                color = 240, 240, 150
                            else:
                                color = 180, 180, 140




                    stay_rect = pygame.Rect(self.square_size * col, self.square_size * row, self.square_size + 1, self.square_size + 1)
                    pygame.draw.rect(self.screen, color, stay_rect)





    def select(self):
        pos = pygame.mouse.get_pos()
        cell = (int(pos[0] / self.square_size), int(pos[1] / self.square_size))
        if cell[0] < 9 and cell[1] < 9:
            if cell == self.current_cell:
                self.current_cell = None
            else:
                self.current_cell = cell

    def button_held(self):
        pos = pygame.mouse.get_pos()
        for i in self.buttons:
            self.buttons[i].is_held(pos, pygame.mouse.get_pressed()[0])

    def button_released(self):
        pos = pygame.mouse.get_pos()
        for i in self.buttons:
            self.buttons[i].is_released(pos)


    def draw_buttons(self):
        for button in self.buttons:
            self.buttons[button].draw()

    def draw_nums(self):
        font = pygame.font.SysFont('Arial', int(self.square_size / 1.5))
        for row in range(9):
            for col in range(9):
                if self.nums[row][col] != 0:
                    text_surface = font.render(str(self.nums[row][col]), True, (0, 0, 0))
                    text_dest = (self.square_size * col + (self.square_size - text_surface.get_rect().width) / 2, self.square_size * row + (self.square_size - text_surface.get_rect().height) / 2)
                    self.screen.blit(text_surface, text_dest)



    def draw_board(self):
        self.screen.fill((255, 255, 255))
        self.highlight_affected()

        self.draw_nums()

        self.draw_grid()
        self.highlight_cell()
        self.draw_buttons()

        pygame.display.flip()

    def is_full(self):
        for i in range(9):
            for j in range(9):
                if self.nums[i][j] == 0:
                    return False
        return True

    def update_board(self, num):
        if self.original[self.current_cell[1]][self.current_cell[0]] == 0:
            self.nums[self.current_cell[1]][self.current_cell[0]] = num

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.nums[i][j] == 0:
                    return i, j
        raise "Error: board is full"

    def check_board(self):
        if self.is_full():
            for i in range(9):
                for j in range(9):
                    if self.solved_board[i][j] != self.nums[i][j]:
                        return False
            return True
        return False


    def reset(self):
        self.nums = copy.deepcopy(self.original)

    def restart(self, difficulty):
        self.nums, self.solved_board = generate_sudoku(9, difficulty)
        self.original = copy.deepcopy(self.nums)

    def quit(self):
        self.running = False





