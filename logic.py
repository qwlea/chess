import pygame

# This class internally handles all of the board logic that's necessary to ensure legal moves are played
class Logic:
    def __init__(self, bd):
        self._board = bd

    # This is a utility function that is used by the other functions of this class
    def verify_legal(self, col, row, legal_moves):
        if 7 >= col >= 0 and 7 >= row >= 0:
            legal_moves.add((col, row))

    # Returns the set of all board spaces a given piece can move to, disregarding potential discovered checks/pins and
    # piece color.
    def get_legal_piece(self, piece, opponent, depth):
        legal_mvs = set()
        tiles = self._board.get_tiles()
        coords = piece.get_coords()
        col = coords[0]
        row = coords[1]

        if piece.get_type() // 2 == 0: # Piece is a king
            self.verify_legal(col + 1, row, legal_mvs)
            self.verify_legal(col, row + 1, legal_mvs)
            self.verify_legal(col + 1, row + 1, legal_mvs)
            self.verify_legal(col + 1, row - 1, legal_mvs)
            self.verify_legal(col - 1, row + 1, legal_mvs)
            self.verify_legal(col - 1, row - 1, legal_mvs)
            self.verify_legal(col - 1, row, legal_mvs)
            self.verify_legal(col, row - 1, legal_mvs)
            # This section is for castling purposes. Castling can only be performed when all of the spaces in between a
            # king and a rook are not under attack by the opposing player and neither the king or rook has moved.
            if depth == 0:
                opp_mvs = self.get_legal_player(opponent)
                if piece.get_n_move() and tiles[col + 3][row].get_piece() is not None and \
                        tiles[col + 3][row].get_piece().get_n_move():
                    can_castle = True
                    for i in range(col, col + 3):
                        if (i, row) in opp_mvs: can_castle = False
                    for i in range(col + 1, col + 3):
                        if tiles[i][row].get_piece() is not None: can_castle = False
                    if can_castle: legal_mvs.add((col + 2, row))
                if piece.get_n_move() and tiles[col - 4][row].get_piece() is not None and \
                        tiles[col - 4][row].get_piece().get_n_move():
                    can_castle = True
                    for i in range(col - 3, col + 1):
                        if (i, row) in opp_mvs: can_castle = False
                    for i in range(col - 3, col):
                        if tiles[i][row].get_piece() is not None: can_castle = False
                    if can_castle: legal_mvs.add((col - 2, row))

        elif piece.get_type() // 2 == 1: # Piece is a queen
            tmp_col = col + 1
            tmp_row = row + 1
            while tmp_col <= 7 and tmp_row <= 7:
                self.verify_legal(tmp_col, tmp_row, legal_mvs)
                if tiles[tmp_col][tmp_row].get_piece() is not None: break
                tmp_col += 1
                tmp_row += 1
            tmp_col = col - 1
            tmp_row = row + 1
            while tmp_col >= 0 and tmp_row <= 7:
                self.verify_legal(tmp_col, tmp_row, legal_mvs)
                if tiles[tmp_col][tmp_row].get_piece() is not None: break
                tmp_col -= 1
                tmp_row += 1
            tmp_col = col + 1
            tmp_row = row - 1
            while tmp_col <= 7 and tmp_row >= 0:
                self.verify_legal(tmp_col, tmp_row, legal_mvs)
                if tiles[tmp_col][tmp_row].get_piece() is not None: break
                tmp_col += 1
                tmp_row -= 1
            tmp_col = col - 1
            tmp_row = row - 1
            while tmp_col >= 0 and tmp_row >= 0:
                self.verify_legal(tmp_col, tmp_row, legal_mvs)
                if tiles[tmp_col][tmp_row].get_piece() is not None: break
                tmp_col -= 1
                tmp_row -= 1
            tmp_col = col + 1
            while tmp_col <= 7:
                self.verify_legal(tmp_col, row, legal_mvs)
                if tiles[tmp_col][row].get_piece() is not None: break
                tmp_col += 1
            tmp_col = col - 1
            while tmp_col >= 0:
                self.verify_legal(tmp_col, row, legal_mvs)
                if tiles[tmp_col][row].get_piece() is not None: break
                tmp_col -= 1
            tmp_row = row + 1
            while tmp_row <= 7:
                self.verify_legal(col, tmp_row, legal_mvs)
                if tiles[col][tmp_row].get_piece() is not None: break
                tmp_row += 1
            tmp_row = row - 1
            while tmp_row >= 0:
                self.verify_legal(col, tmp_row, legal_mvs)
                if tiles[col][tmp_row].get_piece() is not None: break
                tmp_row -= 1

        elif piece.get_type() // 2 == 2: # Piece is a rook
            tmp_col = col + 1
            while tmp_col <= 7:
                self.verify_legal(tmp_col, row, legal_mvs)
                if tiles[tmp_col][row].get_piece() is not None: break
                tmp_col += 1
            tmp_col = col - 1
            while tmp_col >= 0:
                self.verify_legal(tmp_col, row, legal_mvs)
                if tiles[tmp_col][row].get_piece() is not None: break
                tmp_col -= 1
            tmp_row = row + 1
            while tmp_row <= 7:
                self.verify_legal(col, tmp_row, legal_mvs)
                if tiles[col][tmp_row].get_piece() is not None: break
                tmp_row += 1
            tmp_row = row - 1
            while tmp_row >= 0:
                self.verify_legal(col, tmp_row, legal_mvs)
                if tiles[col][tmp_row].get_piece() is not None: break
                tmp_row -= 1

        elif piece.get_type() // 2 == 3: # Piece is a knight
            self.verify_legal(col + 1, row + 2, legal_mvs)
            self.verify_legal(col + 2, row + 1, legal_mvs)
            self.verify_legal(col - 1, row + 2, legal_mvs)
            self.verify_legal(col + 2, row - 1, legal_mvs)
            self.verify_legal(col - 2, row + 1, legal_mvs)
            self.verify_legal(col + 1, row - 2, legal_mvs)
            self.verify_legal(col - 1, row - 2, legal_mvs)
            self.verify_legal(col - 2, row - 1, legal_mvs)

        elif piece.get_type() // 2 == 4: # Piece is a bishop
            tmp_col = col + 1
            tmp_row = row + 1
            while tmp_col <= 7 and tmp_row <= 7:
                self.verify_legal(tmp_col, tmp_row, legal_mvs)
                if tiles[tmp_col][tmp_row].get_piece() is not None: break
                tmp_col += 1
                tmp_row += 1
            tmp_col = col - 1
            tmp_row = row + 1
            while tmp_col >= 0 and tmp_row <= 7:
                self.verify_legal(tmp_col, tmp_row, legal_mvs)
                if tiles[tmp_col][tmp_row].get_piece() is not None: break
                tmp_col -= 1
                tmp_row += 1
            tmp_col = col + 1
            tmp_row = row - 1
            while tmp_col <= 7 and tmp_row >= 0:
                self.verify_legal(tmp_col, tmp_row, legal_mvs)
                if tiles[tmp_col][tmp_row].get_piece() is not None: break
                tmp_col += 1
                tmp_row -= 1
            tmp_col = col - 1
            tmp_row = row - 1
            while tmp_col >= 0 and tmp_row >= 0:
                self.verify_legal(tmp_col, tmp_row, legal_mvs)
                if tiles[tmp_col][tmp_row].get_piece() is not None: break
                tmp_col -= 1
                tmp_row -= 1

        elif piece.get_type() // 2 == 5: # Piece is a pawn
            if piece.get_type() % 2 == 0: # Piece is white
                if piece.get_coords()[1] == 1 and tiles[col][row + 1].get_piece() is None and tiles[col][row + 2].get_piece() is None:
                    legal_mvs.add((col, row + 2))
                if tiles[col][row + 1].get_piece() is None:
                    legal_mvs.add((col, row + 1))
                if col + 1 <= 7 and row + 1 <= 7 and tiles[col + 1][row + 1].get_piece() is not None:
                    legal_mvs.add((col + 1, row + 1))
                if col - 1 >= 0 and row + 1 <= 7 and tiles[col - 1][row + 1].get_piece() is not None:
                    legal_mvs.add((col - 1, row + 1))
                # En passant
                if col + 1 <= 7 and row + 1 <= 7 and tiles[col + 1][row].get_piece() is not None and\
                        tiles[col + 1][row].get_piece().get_type() % 2 != piece.get_type() % 2 and\
                        tiles[col + 1][row].get_piece().get_d_move():
                    legal_mvs.add((col + 1, row + 1))
                if col - 1 >= 0 and row + 1 <= 7 and tiles[col - 1][row].get_piece() is not None and\
                        tiles[col - 1][row].get_piece().get_type() % 2 != piece.get_type() % 2 and\
                        tiles[col - 1][row].get_piece().get_d_move():
                    legal_mvs.add((col - 1, row + 1))
            else: # Piece is black
                if piece.get_coords()[1] == 6 and tiles[col][row - 1].get_piece() is None and tiles[col][row - 2].get_piece() is None:
                    legal_mvs.add((col, row - 2))
                if tiles[col][row - 1].get_piece() is None:
                    legal_mvs.add((col, row - 1))
                if col + 1 <= 7 and row - 1 >= 0 and tiles[col + 1][row - 1].get_piece() is not None:
                    legal_mvs.add((col + 1, row - 1))
                if col - 1 >= 0 and row - 1 >= 0 and tiles[col - 1][row - 1].get_piece() is not None:
                    legal_mvs.add((col - 1, row - 1))
                # En passant
                if col + 1 <= 7 and row - 1 >= 0 and tiles[col + 1][row].get_piece() is not None and\
                        tiles[col + 1][row].get_piece().get_type() % 2 != piece.get_type() % 2 and\
                        tiles[col + 1][row].get_piece().get_d_move():
                    legal_mvs.add((col + 1, row - 1))
                if col - 1 >= 0 and row - 1 >= 0 and tiles[col - 1][row].get_piece() is not None and\
                        tiles[col - 1][row].get_piece().get_type() % 2 != piece.get_type() % 2 and\
                        tiles[col - 1][row].get_piece().get_d_move():
                    legal_mvs.add((col - 1, row - 1))
        return legal_mvs

    # returns the set of all legal moves a player can make, still disregarding discovered checks/pins and piece color
    def get_legal_player(self, player):
        legal_mvs = set()
        for piece in player.get_owned():
            for coords in self.get_legal_piece(piece, None, 1):
                legal_mvs.add(coords)
        return legal_mvs

    # Safely checks if a given move is legal by simulating the play on the board and then reverting all changes
    def safe_check_legal(self, selected_piece, target_tile, player, opponent):
        if target_tile.get_coords() not in self.get_legal_piece(selected_piece, opponent, 0): return False
        if target_tile.get_piece() is not None and\
                target_tile.get_piece().get_type() % 2 == selected_piece.get_type() % 2: return False
        tmp_piece = target_tile.get_piece()
        # This simulates a capture so that capturing a piece that has put the turn player's king in check is legal
        if tmp_piece is not None:
            opponent.get_owned().remove(tmp_piece)
        tmp_tile = selected_piece.get_tile()
        selected_piece.change_tiles(target_tile)
        king_coords = player.get_king().get_coords()
        if king_coords in self.get_legal_player(opponent):
            selected_piece.change_tiles(tmp_tile)
            target_tile.set_piece(tmp_piece)
            if tmp_piece is not None:
                opponent.get_owned().add(tmp_piece)
            return False
        selected_piece.change_tiles(tmp_tile)
        target_tile.set_piece(tmp_piece)
        if tmp_piece is not None:
            opponent.get_owned().add(tmp_piece)
        return True

    # Gets the "true" legal spaces a piece can move to, the spaces that won't leave the player's king in check
    def get_true_legal_piece(self, piece, player, opponent):
        true_legal = set()
        for coords in self.get_legal_piece(piece, opponent, 0):
            if self.safe_check_legal(piece, self._board.get_tile(coords), player, opponent):
                true_legal.add(coords)
        return true_legal

    # Gets the "true" legal spaces all of a player's pieces can move to that won't leave that player's king in check
    def get_true_legal_player(self, player, opponent):
        true_legal = set()
        for piece in player.get_owned():
            for coords in self.get_true_legal_piece(piece, player, opponent):
                true_legal.add(coords)
        return true_legal

    # Checks all possible legal moves a player can make to verify whether the game is in stale/checkmate
    # "NM" == No Mate, "SM" == Stalemate, "CM" == Checkmate
    def safe_check_mate(self, player, opponent):
        for piece in player.get_owned():
            for tile_coords in self.get_legal_piece(piece, opponent, 0):
                if self.safe_check_legal(piece, self._board.get_tile(tile_coords), player, opponent):
                    return "NM"
        king_coords = player.get_king().get_coords()
        if king_coords not in self.get_legal_player(opponent):
            return "SM"
        return "CM"

