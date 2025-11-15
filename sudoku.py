import pygame
from board import Board

def main():
    b = Board(500, 45)
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
                key = event.key
                if key == pygame.K_1:
                    b.update_board(1)
                elif key == pygame.K_2:
                    b.update_board(2)
                elif key == pygame.K_3:
                    b.update_board(3)
                elif key == pygame.K_4:
                    b.update_board(4)
                elif key == pygame.K_5:
                    b.update_board(5)
                elif key == pygame.K_6:
                    b.update_board(6)
                elif key == pygame.K_7:
                    b.update_board(7)
                elif key == pygame.K_8:
                    b.update_board(8)
                elif key == pygame.K_9:
                    b.update_board(9)


                elif event.key == pygame.K_ESCAPE:
                    b.quit()
            if event.type == pygame.QUIT:
                b.quit()


        b.button_held()

        clock.tick(20)


if __name__ == "__main__":
    main()