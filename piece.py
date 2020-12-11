import pygame
from random import randint

# Class that represents the individual pieces on the board. This class also internally handles moving pieces around on the board.
class Piece(pygame.sprite.Sprite):
    WKING = 0
    BKING = 1
    # ^--^--^ // 2 == 0
    WQUEEN = 2
    BQUEEN = 3
    # ^--^--^ // 2 == 1
    WROOK = 4
    BROOK = 5
    # ^--^--^ // 2 == 2
    WKNIGHT = 6
    BKNIGHT = 7
    # ^--^--^ // 2 == 3
    WBISHOP = 8
    BBISHOP = 9
    # ^--^--^ // 2 == 4
    WPAWN = 10
    BPAWN = 11
    # ^--^--^ // 2 == 5

    def __init__(self, p_type, start_coords, board, player):
        super().__init__()
        self._not_moved = True # Only here for castling purposes
        self._moved_double = False # Only here for pawns with en passant
        self._pawn = p_type // 2 == 5 # Only here to differentiate promoted pawns from other pieces for the score
        self._type = p_type
        start_tile = board.get_tile(start_coords)
        self._tile = start_tile
        if p_type == Piece.WKING:
            self.image = pygame.image.load("Sprites/white_king.png")
        if p_type == Piece.BKING:
            self.image = pygame.image.load("Sprites/black_king.png")
        if p_type == Piece.WQUEEN:
            self.image = pygame.image.load("Sprites/white_queen.png")
        if p_type == Piece.BQUEEN:
            self.image = pygame.image.load("Sprites/black_queen.png")
        if p_type == Piece.WROOK:
            self.image = pygame.image.load("Sprites/white_rook.png")
        if p_type == Piece.BROOK:
            self.image = pygame.image.load("Sprites/black_rook.png")
        if p_type == Piece.WKNIGHT:
            self.image = pygame.image.load("Sprites/white_knight.png")
        if p_type == Piece.BKNIGHT:
            self.image = pygame.image.load("Sprites/black_knight.png")
        if p_type == Piece.WBISHOP:
            self.image = pygame.image.load("Sprites/white_bishop.png")
        if p_type == Piece.BBISHOP:
            self.image = pygame.image.load("Sprites/black_bishop.png")
        if p_type == Piece.WPAWN:
            self.image = pygame.image.load("Sprites/white_pawn.png")
        if p_type == Piece.BPAWN:
            self.image = pygame.image.load("Sprites/black_pawn.png")
        posx = start_tile.get_area()[0]
        posy = start_tile.get_area()[1]
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        start_tile.set_piece(self)
        player.get_owned().add(self)

    def get_n_move(self):
        return self._not_moved

    def get_d_move(self):
        return self._moved_double

    def is_pawn(self):
        return self._pawn

    def get_type(self):
        return self._type

    def get_tile(self):
        return self._tile

    def get_coords(self):
        return self._tile.get_coords()

    def set_pos(self, posx, posy):
        self.rect.x = posx
        self.rect.y = posy

    def restore_pos(self):
        self.rect.x = self.get_tile().get_area()[0]
        self.rect.y = self.get_tile().get_area()[1]

    def change_tiles(self, new_tile):
        new_x = new_tile.get_area()[0]
        new_y = new_tile.get_area()[1]
        self.set_pos(new_x, new_y)
        self._tile.set_piece(None)
        self._tile = new_tile
        self._tile.set_piece(self)

    # Called whenver a pawn needs to be promoted. Only allows pawns to be promoted to queen although very rarely other
    # pieces can be a better choice due to potential stalemates and knight checks
    def promote(self):
        self._type = 2 + self._type % 2
        self.image = [pygame.image.load("Sprites/white_queen.png"), pygame.image.load("Sprites/black_queen.png")][self._type % 2]

    # This method is called whenver a move has been verified as being legal and has been made by the turn player.
    def change_tiles_final(self, new_tile, player, opponent, board, logic, log, turn):
        self._not_moved = False
        # Various variables that are used to help write the turn line for the log file
        line = ""
        player_name = ["White", "Black"][player.get_id()]
        capture = False
        castle = False
        passant = False
        current_tile_id = self.get_tile().get_id()
        new_tile_id = new_tile.get_id()
        t = ["k", "q", "r", "n", "b", "p"][self.get_type() // 2] # t == type
        ct = "" # ct == capture type
        mv = ""
        line += f"Turn {turn + 1}, {player_name}: "
        # Castling implementation
        if self.get_type() // 2 == 0 and new_tile.get_coords()[0] == self.get_coords()[0] - 2 or\
                self.get_type() // 2 == 0 and new_tile.get_coords()[0] == self.get_coords()[0] + 2:
            if new_tile.get_coords()[0] == self.get_coords()[0] + 2:
                board.get_tiles()[self.get_coords()[0] + 3][self.get_coords()[1]].get_piece().change_tiles(board.get_tiles()[self.get_coords()[0] + 1][self.get_coords()[1]])
                castle = True
                mv = "O-O"
            if new_tile.get_coords()[0] == self.get_coords()[0] - 2:
                board.get_tiles()[self.get_coords()[0] - 4][self.get_coords()[1]].get_piece().change_tiles(board.get_tiles()[self.get_coords()[0] - 1][self.get_coords()[1]])
                castle = True
                mv = "O-O-O"
        if new_tile.get_piece() is not None:
            if new_tile.get_piece().is_pawn(): player.record_capture(4)
            else: player.record_capture(new_tile.get_piece().get_type() // 2 - 1)
            opponent.get_owned().remove(new_tile.get_piece())
            capture = True
            ct = ["", "q", "r", "n", "b", "p"][new_tile.get_piece().get_type() // 2]
        if self.get_type() == 10: # En passant check for white pawns
            tile_piece = board.get_tiles()[new_tile.get_coords()[0]][new_tile.get_coords()[1] - 1].get_piece()
            if tile_piece is not None and tile_piece.get_d_move() and tile_piece.get_type() % 2 != self.get_type() % 2:
                player.record_capture(4) # Records a pawn capture
                opponent.get_owned().remove(tile_piece)
                board.get_tiles()[new_tile.get_coords()[0]][new_tile.get_coords()[1] - 1].set_piece(None)
                passant = True
        if self.get_type() == 11: # En passant check for black pawns
            tile_piece = board.get_tiles()[new_tile.get_coords()[0]][new_tile.get_coords()[1] + 1].get_piece()
            if tile_piece is not None and tile_piece.get_d_move() and tile_piece.get_type() % 2 != self.get_type() % 2:
                player.record_capture(4) # Records a pawn capture
                opponent.get_owned().remove(tile_piece)
                board.get_tiles()[new_tile.get_coords()[0]][new_tile.get_coords()[1] + 1].set_piece(None)
                passant = True
        old_tile = self.get_tile()
        # Removes all double moved pawns since en passant only works the turn that particular pawn is doubly moved
        for piece in opponent.get_owned():
            piece._moved_double = False
        self.change_tiles(new_tile)
        # Specifies if a pawn has made a double move this turn. This is necessary for en passant.
        if self.get_type() == 10 and self.get_coords()[1] == old_tile.get_coords()[1] + 2\
                or self.get_type() == 11 and self.get_coords()[1] == old_tile.get_coords()[1] - 2:
            self._moved_double = True
        # Promotes any pawns that reach the extremeties of the board to queens
        if self.get_type() // 2 == 5 and self.get_coords()[1] == 7 or\
                self.get_type() // 2 == 5 and self.get_coords()[1] == 0:
            self.promote()
        check = opponent.get_king().get_coords() in logic.get_legal_player(player)
        sound = None
        if castle:
            line += mv
            sound = pygame.mixer.Sound(file="Sounds/Castle.wav")
        elif passant:
            line += f"p{current_tile_id}-/-{new_tile_id}"
            sound = pygame.mixer.Sound(file="Sounds/EnPassant.wav")
        elif capture:
            line += f"{t}{current_tile_id}-x-{ct}{new_tile_id}"
            sound = pygame.mixer.Sound(file=f"Sounds/Move{randint(1, 4)}.wav")
        else:
            line += f"{t}{current_tile_id}->{new_tile_id}"
            sound = pygame.mixer.Sound(file=f"Sounds/Move{randint(1, 4)}.wav")
        if check:
            line += "+"
            sound = pygame.mixer.Sound(file="Sounds/Check.wav")
        log.write_line(line)
        sound.play()
