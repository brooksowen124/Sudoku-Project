import pygame
from board import Board

def main():
    b = Board(500, 10)
    clock = pygame.time.Clock()
    running = True
    while running:
        b.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    b.click()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False

        clock.tick(10)


if __name__ == "__main__":
    main()