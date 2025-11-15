import pygame
import copy


from sudoku_generator import generate_sudoku
from button import Button

class Board:
    def __init__(self, size, difficulty):
        # constructor for a Board object, sets the screen, size of the screen, the difficulty (number of cells to be removed), and the current cell that is selected
        self.screen = pygame.display.set_mode((size + 2, size + size * 2 / 9))
        pygame.display.set_caption("Sudoku")
        self.size = size
        self.square_size = size / 9
        self.difficulty = difficulty
        self.current_cell = None

        # initializes the randomly generated board
        self.nums = generate_sudoku(9, difficulty)
        # stores the original board as a deep copy in case we reset the board
        self.original = copy.deepcopy(self.nums)
        self.sketch = [[0 for _ in range(9)] for _ in range(9)]

        self.running = True

        # initializes the buttons on the board
        self.buttons = {
            "Reset": Button(self.screen, size / 4 * 1, self.size * 10 / 9, self.square_size * 1.6, self.square_size * 0.8, "Reset", int(self.square_size / 2.7), self.reset),
            "Restart": Button(self.screen, size / 4 * 2, self.size * 10 / 9, self.square_size * 1.6, self.square_size * 0.8, "Restart", int(self.square_size / 2.7), self.restart),
            "Exit": Button(self.screen, size / 4 * 3, self.size * 10 / 9, self.square_size * 1.6, self.square_size * 0.8, "Exit", int(self.square_size / 2.7), self.quit)
        }

        pygame.font.init()

        self.num_font = pygame.font.SysFont('Arial', int(self.square_size / 1.5))
        self.sketch_font = pygame.font.SysFont('Arial', int(self.square_size / 2.5))




    def draw_grid(self):
        # draws the 9x9 grid on the screen
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
        # highlights the cell that is currently selected
        if self.current_cell is not None:
            rect = pygame.Rect(self.current_cell[0] * self.square_size, self.current_cell[1] * self.square_size, self.square_size + 2, self.square_size + 2)
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 4)

    def highlight_affected(self):
        # highlights the row and column and box of the cell that is currently selected
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
        # updates the 9x9 list of the sketches
        if self.original[self.current_cell[1]][self.current_cell[0]] == 0:
            self.sketch[self.current_cell[1]][self.current_cell[0]] = num

    def set_sketch(self):
        # sets the 9x9 list of the sketches
        self.nums[self.current_cell[1]][self.current_cell[0]] = self.sketch[self.current_cell[1]][self.current_cell[0]]
        self.sketch[self.current_cell[1]][self.current_cell[0]] = 0

    def clear_cell(self):
        # clears the current cell
        self.nums[self.current_cell[1]][self.current_cell[0]] = 0
        self.sketch[self.current_cell[1]][self.current_cell[0]] = 0


    def select(self):
        # allows the user to select which cell to edit when they click on it
        pos = pygame.mouse.get_pos()
        cell = (int(pos[0] / self.square_size), int(pos[1] / self.square_size))
        if cell[0] < 9 and cell[1] < 9:
            if cell == self.current_cell:
                self.current_cell = None
            else:
                self.current_cell = cell

    def button_held(self):
        # detects if the user is holding their mouse button at a certain position
        pos = pygame.mouse.get_pos()
        for i in self.buttons:
            self.buttons[i].is_held(pos, pygame.mouse.get_pressed()[0])

    def button_released(self):
        # detects when the user releases a button at a certain position
        pos = pygame.mouse.get_pos()
        for i in self.buttons:
            self.buttons[i].is_released(pos)


    def draw_buttons(self):
        # draws the buttons on the screen
        for button in self.buttons:
            self.buttons[button].draw()

    def draw_nums(self):
        # draws the numbers on the screen
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
        # draws the board onto the screen
        self.screen.fill((255, 255, 255))
        self.highlight_affected()

        self.draw_nums()

        self.draw_grid()
        self.highlight_cell()
        self.draw_buttons()

        pygame.display.flip()

    def is_full(self):
        # detects if every element of the board contains a number
        for i in range(9):
            for j in range(9):
                if self.nums[i][j] == 0:
                    return False
        return True


    def find_empty(self):
        # finds any empty cells on the board
        for i in range(9):
            for j in range(9):
                if self.nums[i][j] == 0:
                    return i, j
        raise "Error: board is full"

    def check_board(self):
        # checks to ensure that every row, box, and column in the board is valid
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
        # resets the board to the original position
        self.nums = copy.deepcopy(self.original)

    def restart(self):
        # generates a new random sudoku board
        self.nums = generate_sudoku(9, self.difficulty)
        self.original = copy.deepcopy(self.nums)

    def quit(self):
        # quits the main board loop
        self.running = False





