import pygame
from tile import *
from player import *
from ai import *
from logic import Logic

# This class' main responsibility is that of generating the board surface as well as the individual tiles that make up
# the board when the program starts. It is also used by the logic class to calculate move legalities.
class Board:
    def __init__(self, screen_w, screen_h, choice, board_state):
        screen_w_midpoint = screen_w / 2
        screen_h_midpoint = screen_h / 2
        self._TL = (screen_w_midpoint - 256, screen_h_midpoint - 256) # TL == Top-Left Corner
        self._SURFACE = pygame.Surface((512, 512)) # The board surface is made up of 64 64x64 squares
        self._TILES = []
        self.PLAYERS = []
        self.PLAYERS.append(Player(0, self))
        if choice == "0" : self.PLAYERS.append(Player(1, self))
        else: self.PLAYERS.append(MiniMax(1, self, Logic(self)))
        self.turn = 0
# This part of the init method creates all of the tiles on the board and assigns them their coords and ids.
# The drawn upon surface is blitted to the screen every frame in the main gameplay loop from this class.
        for i in range(0, 8):
            self._TILES.append([])
            for j in range(0, 8):
                self._TILES[i].append(Tile((i, j), self._TL))
                left = 64 * i
                top = 64 * j
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self._SURFACE, (238, 195, 164), (left, top, 64, 64))
                else:
                    pygame.draw.rect(self._SURFACE, (143, 86, 59), (left, top, 64, 64))
        with open(board_state, "r") as f:
            state = f.readlines()
        for idx, row in enumerate(state):
            if idx <= 7:
                chars = list(state[idx])
                for i in range(8):
                    coords = (i, 7 - idx)
                    piece = chars[i * 2] + chars[i * 2 + 1]
                    if piece != "||":
                        for j in range(12):
                            if piece == ["WK", "BK", "WQ", "BQ", "WR", "BR", "WN", "BN", "WB", "BB", "WP", "BP"][j]:
                                tmp = Piece(j, coords, self, self.PLAYERS[j % 2])
                                if j == 0 or j == 1: self.PLAYERS[j % 2].__setattr__("_king", tmp)
                                break
            else:
                self.turn = int(state[idx][:])
                break

    # __repr__() is reserved for creating new board save save states. It isn't the easiest to read, as there are no
    # spaces between any of the lines or tiles of the board, but it is much easier to process than a typical string
    # interpretation of the board.
    def __repr__(self):
        brd = ""
        for j in range(7, -1, -1):
            row = ""
            for i in range(8):
                piece = self._TILES[i][j].get_piece()
                if piece: row += ["WK", "BK", "WQ", "BQ", "WR", "BR", "WN", "BN", "WB", "BB", "WP", "BP"][piece.get_type()]
                else: row += "||"
            brd += row + "\n"
        brd += str(self.turn)
        return brd

    # String version of the board, quite a bit more readable than the __repr__() version which is reserved for creating
    # new save states of the board.
    def __str__(self):
        brd = ""
        for j in range(7, -1, -1):
            row = []
            for i in range(8):
                piece = self._TILES[i][j].get_piece()
                if piece: row.append(["WK", "BK", "WQ", "BQ", "WR", "BR", "WN", "BN", "WB", "BB", "WP", "BP"][piece.get_type()])
                else: row.append("||")
            brd += str(row) + "\n"
        return brd

    def tur_play(self):
        return self.PLAYERS[self.turn % 2]

    def opp_play(self):
        return self.PLAYERS[(self.turn + 1) % 2]

    def get_tl(self):
        return self._TL

    def get_surface(self):
        return self._SURFACE

    def get_tiles(self):
        return self._TILES

    # Returns the tile at the designated coordinates (x, y) where 0 represents A in x and 1 in y on the board
    def get_tile(self, coords):
        return self._TILES[coords[0]][coords[1]]

    def draw_board(self):
        for i in range(0, 8):
            for j in range(0, 8):
                left = 64 * i
                top = 64 * j
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self._SURFACE, (238, 195, 164), (left, top, 64, 64))
                else:
                    pygame.draw.rect(self._SURFACE, (143, 86, 59), (left, top, 64, 64))
