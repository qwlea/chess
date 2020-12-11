from pygame import *
from board import *
from logic import *
from text import *
from log import *
from ai import *

class Chess:
    def __init__(self, choice="0", board_state="States/default.txt"):
        # Launches Pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(4)
        pygame.mouse.set_visible(False)
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont(None, 56)

        # Sets up the display
        disp_inf = pygame.display.Info()
        screen_w = disp_inf.current_w
        screen_h = disp_inf.current_h
        self._window = pygame.display.set_mode((screen_w, screen_h), pygame.DOUBLEBUF)
        pygame.display.set_caption("Cheap Chess, Deep Chess")

        # Creation of the canvas overlay that is used on top of the window
        self._canvas = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA, 32)

        # Creation of the game board and logic for the chess class. The board internally initializes all of the
        # pieces and both players as well, based on the board state and choice passed to the game on startup.
        self._board = Board(screen_w, screen_h, choice, board_state)
        self._logic = Logic(self._board)

        # Creates the text elements for the game board
        self._text = []
        self._turn_text = []
        left = self._board.get_tl()[0] - 48
        bottom = self._board.get_tl()[1] + 528
        self._turn_text.append(Text(self._font, "White's Turn", (0, 0, 0, 255), (127, 190, 127, 255), left + 190, bottom - 576))
        self._turn_text.append(Text(self._font, "Black's Turn", (0, 0, 0, 255), (127, 190, 127, 255), left + 190, bottom - 576))
        for i in range(8):
            self._text.append(Text(self._font, str(chr(65 + i)), (0, 0, 0, 255), (127, 190, 127, 255), left + (i + 1) * 64, bottom))
        for i in range(8):
            self._text.append(Text(self._font, str(8 - i), (0, 0, 0, 255), (127, 190, 127, 255), left, bottom - (8 - i) * 64))

        # Creation of the log that stores the turn information
        self._log = Log()


    def run(self):
        done = False
        s_p = None # == Selected Piece
        legals = set()
        cursor_img = pygame.image.load("Sprites/open_hand.png")
        # ----------Event Handler----------
        while not done:
            # -----AI turn implementation-----
            if type(self._board.tur_play()) is MiniMax:
                ai = self._board.tur_play()
                pl = self._board.opp_play()
                move = ai.randmove(pl, self._board)
                selected_piece = self._board.get_tile(move[0]).get_piece()
                target_tile = self._board.get_tile(move[1])
                selected_piece.change_tiles_final(target_tile, ai, pl, self._board, self._logic, self._log, self._board.turn)
                self._board.turn += 1
                res = self._logic.safe_check_mate(pl, ai)
                if res == "CM" and self._board.turn % 2 == 0:
                    self._log.write_line("Black wins by checkmate!")
                    done = True
                elif res == "CM":
                    self._log.write_line("White wins by checkmate!")
                    done = True
                elif res == "SM":
                    self._log.write_line("It's a tie by stalemate!")
                    done = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    done = True

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                    with open("States/new_save.txt", "w") as f:
                        f.write(self._board.__repr__())

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                    mouse_x = pos[0]
                    mouse_y = pos[1]
                    for piece in self._board.tur_play().get_owned():
                        if piece.rect.collidepoint(mouse_x, mouse_y):
                            s_p = piece
                            legals = self._logic.get_true_legal_piece(s_p, self._board.tur_play(), self._board.opp_play())
                            cursor_img = pygame.image.load("Sprites/closed_hand.png")
                            break

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if s_p is not None:
                        player = self._board.tur_play()
                        opponent = self._board.opp_play()
                        pos = event.pos
                        mouse_x = pos[0]
                        mouse_y = pos[1]
                        tl = self._board.get_tl()
                        left = tl[0]
                        top = tl[1]
                        right = left + 512  # 8 64x64 squares
                        bottom = top + 512  # 8 64x64 squares
                        if left < mouse_x < right and top < mouse_y < bottom:
                            x_offset = mouse_x - tl[0]
                            y_offset = mouse_y - tl[1]
                            x_coord = int(x_offset // 64)
                            y_coord = 7 - int(y_offset // 64)
                            t_t = self._board.get_tile((x_coord, y_coord))  # == Target Tile
                            if (x_coord, y_coord) in legals:
                                s_p.change_tiles_final(t_t, player, opponent, self._board, self._logic, self._log, self._board.turn)
                                self._board.turn += 1
                                res = self._logic.safe_check_mate(opponent, player)
                                if res == "CM" and self._board.turn % 2 == 0:
                                    self._log.write_line("Black wins by checkmate!")
                                    done = True
                                elif res == "CM":
                                    self._log.write_line("White wins by checkmate!")
                                    done = True
                                elif res == "SM":
                                    self._log.write_line("It's a tie by stalemate!")
                                    done = True
                            else:
                                s_p.restore_pos()
                                if not s_p.rect.collidepoint(pygame.mouse.get_pos()):
                                    pygame.mixer.Sound(file="Sounds/no.wav").play()
                        else:
                            s_p.restore_pos()
                        s_p = None
                        legals.clear()
                        cursor_img = pygame.image.load("Sprites/open_hand.png")

            # ----------Graphics Renderer----------
            self._canvas.fill((127, 190, 127, 255))
            self._canvas.blit(self._board.get_surface(), self._board.get_tl())
            for coords in legals:
                x = self._board.get_tl()[0] + coords[0] * 64
                y = self._board.get_tl()[1] + (7 - coords[1]) * 64
                s = pygame.Surface((64, 64))
                s.fill((255, 0, 255, 128))
                s.set_alpha(128)
                self._canvas.blit(s, (x, y))
            for text in self._text:
                text.paste(self._canvas)
            self._turn_text[self._board.turn % 2].paste(self._canvas)
            for player in self._board.PLAYERS:
                for piece in player.get_owned():
                    if piece != s_p:
                        self._canvas.blit(piece.image, piece.rect)
            if s_p is not None:
                mouse_pos = pygame.mouse.get_pos()
                # Subtract 32 pixels from each axis to center the image onto the cursor.
                posx = mouse_pos[0] - 32
                posy = mouse_pos[1] - 32
                s_p.set_pos(posx, posy)
                self._canvas.blit(s_p.image, s_p.rect)
            pos = pygame.mouse.get_pos()
            self._canvas.blit(cursor_img, (pos[0] - 3, pos[1] - 8))
            self._window.blit(self._canvas, (0, 0))
            pygame.display.flip()
            self._clock.tick(60)

if __name__ == '__main__':
    import sys
    chess = None # Used to keep chess in the scope of the following if statements
    arg_count = len(sys.argv)
    if arg_count > 3:
        print("Incompatible number of arguments given upon startup.")
        print("For information on how to run chess.py in the terminal, refer to the readme file located in the folder.")
        exit(1)
    elif arg_count == 1:
        chess = Chess()
    elif arg_count == 2:
        chess = Chess(sys.argv[1])
    elif arg_count == 3:
        chess = Chess(sys.argv[1], sys.argv[2])
    chess.run()
    chess._log.create_log()