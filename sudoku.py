import pygame
from board import Board

def main():
    b = Board(500)
    clock = pygame.time.Clock()
    while b.playing:
        while b.start_screen:

            b.draw_start()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        b.quit_game()


                if event.type == pygame.MOUSEBUTTONUP:
                    b.button_released(b.start_buttons)

                if event.type == pygame.QUIT:
                    b.quit_game()

            b.button_held(b.start_buttons)
            clock.tick(20)

        while b.running:
            b.draw_board()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        b.select()
                elif event.type == pygame.MOUSEBUTTONUP:
                    b.button_released(b.game_buttons)

                elif event.type == pygame.KEYDOWN:
                    key = event.key

                    if key == pygame.K_UP:
                        b.current_cell = (b.current_cell[0], max(b.current_cell[1] - 1, 0))
                    elif key == pygame.K_DOWN:
                        b.current_cell = (b.current_cell[0], min(b.current_cell[1] + 1, 8))
                    elif key == pygame.K_LEFT:
                        b.current_cell = (max(b.current_cell[0] - 1, 0), b.current_cell[1])
                    elif key == pygame.K_RIGHT:
                        b.current_cell = (min(b.current_cell[0] + 1, 8), b.current_cell[1])

                    if key == pygame.K_1:
                        b.update_sketch(1)
                    elif key == pygame.K_2:
                        b.update_sketch(2)
                    elif key == pygame.K_3:
                        b.update_sketch(3)
                    elif key == pygame.K_4:
                        b.update_sketch(4)
                    elif key == pygame.K_5:
                        b.update_sketch(5)
                    elif key == pygame.K_6:
                        b.update_sketch(6)
                    elif key == pygame.K_7:
                        b.update_sketch(7)
                    elif key == pygame.K_8:
                        b.update_sketch(8)
                    elif key == pygame.K_9:
                        b.update_sketch(9)
                    elif key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
                        b.clear_cell()

                    elif key == pygame.K_RETURN:
                        b.set_sketch()

                    elif event.key == pygame.K_ESCAPE:
                        b.quit()

                    if b.is_full():
                        if b.check_board():
                            print("Board is solved")
                            b.won()
                        else:
                            print("Board is not solved, lock in g")



                if event.type == pygame.QUIT:
                    b.quit_game()

            b.button_held(b.game_buttons)
            clock.tick(20)

        while b.end_screen:

            b.draw_end()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        b.quit_game()


                if event.type == pygame.MOUSEBUTTONUP:
                    b.button_released(b.end_buttons)

                if event.type == pygame.QUIT:
                    b.quit_game()

            b.button_held(b.end_buttons)
            clock.tick(20)


if __name__ == "__main__":
    main()