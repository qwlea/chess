import pygame

# Class that represents each individual tile on the board
class Tile:
    def __init__(self, coords, board_tl):
        self._COORDS = coords
        letter = chr(65 + coords[0])
        number = coords[1] + 1
        self._ID = str(letter) + str(number)
        board_left = board_tl[0]
        board_bottom = board_tl[1] + 512
        self._AREA = pygame.Rect(board_left + 64 * coords[0], board_bottom - 64 * (coords[1] + 1), 64, 64)
        self._piece = None


    def get_coords(self):
        return self._COORDS

    def get_id(self):
        return self._ID

    def get_area(self):
        return self._AREA

    def get_piece(self):
        return self._piece

    def set_piece(self, piece):
        self._piece = piece