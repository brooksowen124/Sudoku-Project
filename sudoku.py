import pygame
from board import Board

def main():
    b = Board(400, 45)
    clock = pygame.time.Clock()
    while b.running:
        b.draw_board()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    b.select()
            elif event.type == pygame.MOUSEBUTTONUP:
                b.button_released()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    b.quit()
            if event.type == pygame.QUIT:
                b.quit()


        b.button_held()

        clock.tick(20)


if __name__ == "__main__":
    main()