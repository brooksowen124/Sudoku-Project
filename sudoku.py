import pygame
from board import Board

def main():
    b = Board(700, 10)
    clock = pygame.time.Clock()
    running = True
    while running:
        b.draw_board()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    b.click()
            elif event.type == pygame.MOUSEBUTTONUP:
                b.button_released()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False


        b.button_held()

        clock.tick(10)


if __name__ == "__main__":
    main()