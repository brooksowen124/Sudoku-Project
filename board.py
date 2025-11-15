import pygame
import copy

from sudoku_generator import generate_sudoku
from button import Button

class Board:
    def __init__(self, size):
        self.screen = pygame.display.set_mode((size + 2, size + size * 2 / 9))
        pygame.display.set_caption("Sudoku")
        self.size = size
        self.square_size = size / 9
        self.current_cell = None

        self.playing = True
        self.running = True
        self.start_screen = True
        self.end_screen = False

        self.difficulty = 0

        self.nums, self.solved_board = None, None

        self.original = None
        self.sketch = None

        self.game_buttons = {
            "Reset": Button(self.screen, size / 4 * 1, self.size * 10 / 9, self.square_size * 1.6, self.square_size * 0.8, "Reset", int(self.square_size / 2.7), self.reset),
            "Restart": Button(self.screen, size / 4 * 2, self.size * 10 / 9, self.square_size * 1.6, self.square_size * 0.8, "Restart", int(self.square_size / 2.7), self.restart),
            "Exit": Button(self.screen, size / 4 * 3, self.size * 10 / 9, self.square_size * 1.6, self.square_size * 0.8, "Exit", int(self.square_size / 2.7), self.quit)
        }

        self.start_buttons = {
            "Easy": Button(self.screen, size / 4 * 1, self.size / 2, self.square_size * 2, self.square_size * 0.8, "Easy", int(self.square_size / 2), lambda: self.set_difficulty(1)),
            "Medium": Button(self.screen, size / 4 * 2, self.size / 2, self.square_size * 2, self.square_size * 0.8, "Medium", int(self.square_size / 2), lambda: self.set_difficulty(40)),
            "Hard": Button(self.screen, size / 4 * 3, self.size / 2, self.square_size * 2,self.square_size * 0.8, "Hard", int(self.square_size / 2), lambda: self.set_difficulty(50)),
            "Exit": Button(self.screen, size / 4 * 3, self.size * 10 / 9, self.square_size * 1.6, self.square_size * 0.8, "Exit", int(self.square_size / 2.7), self.quit_game)

        }

        self.end_buttons = {
            "Restart": Button(self.screen, size / 3 * 1, self.size / 3 * 2, self.square_size * 2, self.square_size * 0.8,"Restart", int(self.square_size / 2), self.quit),
            "Exit": Button(self.screen, size / 3 * 2, self.size / 3 * 2, self.square_size * 2, self.square_size * 0.8,"Exit", int(self.square_size / 2), self.quit_game),

        }


        pygame.font.init()

        self.num_font = pygame.font.SysFont('Arial', int(self.square_size / 1.5))
        self.sketch_font = pygame.font.SysFont('Arial', int(self.square_size / 2.5))

    def start(self):
        self.start_screen = False

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

        self.nums, self.solved_board = generate_sudoku(9, difficulty)

        self.original = copy.deepcopy(self.nums)
        self.sketch = [[0 for _ in range(9)] for _ in range(9)]
        self.start()

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


    def update_sketch(self, num):
        if self.original[self.current_cell[1]][self.current_cell[0]] == 0:
            self.sketch[self.current_cell[1]][self.current_cell[0]] = num

    def set_sketch(self):
        self.nums[self.current_cell[1]][self.current_cell[0]] = self.sketch[self.current_cell[1]][self.current_cell[0]]
        self.sketch[self.current_cell[1]][self.current_cell[0]] = 0

    def clear_cell(self):
        self.nums[self.current_cell[1]][self.current_cell[0]] = 0
        self.sketch[self.current_cell[1]][self.current_cell[0]] = 0


    def select(self):
        pos = pygame.mouse.get_pos()
        cell = (int(pos[0] / self.square_size), int(pos[1] / self.square_size))
        if cell[0] < 9 and cell[1] < 9:
            if cell == self.current_cell:
                self.current_cell = None
            else:
                self.current_cell = cell

    @staticmethod
    def button_held(buttons):
        pos = pygame.mouse.get_pos()
        for i in buttons:
            buttons[i].is_held(pos, pygame.mouse.get_pressed()[0])

    @staticmethod
    def button_released(buttons):
        pos = pygame.mouse.get_pos()
        for i in buttons:
            buttons[i].is_released(pos)

    @staticmethod
    def draw_buttons(buttons):
        for button in buttons:
            buttons[button].draw()

    def draw_nums(self):
        for row in range(9):
            for col in range(9):
                if self.nums[row][col] != 0:
                    text_surface = self.num_font.render(str(self.nums[row][col]), True, (0, 0, 0))
                    text_dest = (self.square_size * col + (self.square_size - text_surface.get_rect().width) / 2, self.square_size * row + (self.square_size - text_surface.get_rect().height) / 2)
                    self.screen.blit(text_surface, text_dest)
                elif self.sketch[row][col] != 0:
                    text_surface = self.sketch_font.render(str(self.sketch[row][col]), True, (90, 90, 90))
                    text_dest = (self.square_size * col + (self.square_size - text_surface.get_rect().width) / 4, self.square_size * row + (self.square_size - text_surface.get_rect().height) / 4)
                    self.screen.blit(text_surface, text_dest)




    def draw_board(self):
        self.screen.fill((255, 255, 255))
        self.highlight_affected()

        self.draw_nums()

        self.draw_grid()
        self.highlight_cell()
        self.draw_buttons(self.game_buttons)

        pygame.display.flip()

    def draw_start(self):
        self.screen.fill((255, 255, 255))

        self.draw_buttons(self.start_buttons)

        pygame.display.flip()


    def draw_end(self):
        self.screen.fill((255, 255, 255))

        self.draw_buttons(self.end_buttons)

        pygame.display.flip()


    def is_full(self):
        for i in range(9):
            for j in range(9):
                if self.nums[i][j] == 0:
                    return False
        return True


    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.nums[i][j] == 0:
                    return i, j
        raise "Error: board is full"

    def check_board(self):
        for row in self.nums:
            if sorted(row) != list(range(1, 10)):
                return False
        for col in range(9):
            column = [self.nums[row][col] for row in range(9)]
            if sorted(column) != list(range(1, 10)):
                return False
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        box.append(self.nums[r][c])
                if sorted(box) != list(range(1, 10)):
                    return False
        return True


    def reset(self):
        self.nums = copy.deepcopy(self.original)

    def restart(self):
        self.nums, self.solved_board = generate_sudoku(9, self.difficulty)
        self.original = copy.deepcopy(self.nums)

    def quit(self):
        self.running = False
        self.end_screen = False
        self.start_screen = True

    def quit_game(self):
        self.quit()
        self.start_screen = False
        self.end_screen = False
        self.playing = False

    def won(self):
        self.quit()
        self.end_screen = True




