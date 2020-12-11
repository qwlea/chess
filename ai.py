from player import Player
import copy
from random import randint

# This AI class uses MiniMax Alpha-Beta Pruning in order to find the best possible move(s) each turn.
class MiniMax(Player):
    def __init__(self, pid, board, logic):
        super().__init__(pid, board)
        self._logic = logic

# Board evaluations are handled symmetrically, that is to say, every action that adds to a certain player's score will
# subtract from the opponent's score by the same amount. Score evaluations are handled as follows:
# Piece-Points Values:
# Queen = 90, Rook = 50, Knight = 30, Bishop = 32, Pawn = 10
# Although Bishops have the same literal score as knights in chess, 3:3, bishops are generally considered to be slightly
# more valuable than knights in mid to late game board states as they have much more mobility and have the potential to
# dominate opened-up boards by covering many more squares than a knight could.

# Putting a king in check: +6 points
# Putting a king in check can be very advantageous for gaining a tempo and potentially netting free pieces, but the value
# of checking a player's king cannot be overevaluated lest terrible moves such as free pawn sacrifices become commonplace

# Attacking unprotected pieces: +(0.8 * Piece-Points)
# This one is pretty self explanatory. Attacking unprotected pieces tends to be very strong and forces the opponent to
# react accordingly in order to save the piece. Attacking several unprotected pieces at a time can lead to game-winning
# exchanges that quickly lead to victory.

# Attacking protected pieces: +max(0, 0.2 * Piece-Points-Diff)
# Attacking protected pieces can also be advantageous for aggressive pushes and complicating the board state for the
# opponent.

# Protecting pieces: +(0.5 * Piece-Points)
# For the very reasons mentioned above, protecting pieces is very important. Leaving too many hanging pieces can swiftly
# lead to losing board states. Kings and queens will not be taken into account when calculating this value, as a queen
# can only trade evenly or worse with other pieces and there is no way to "protect" the king in this sense because the
# king cannot be captured. Pawns get a 1.5 value modifier for being protected as it can often be more advantageous to
# protect your pawns with your pieces than it is to protect your pieces with your pawns

# Pieces in center 16 tiles: +2 points
# Controlling the center of the board is one of the most important strategies in chess as almost all of the pieces have
# the possibility of being much more active when positioned around the center of the board.

# Pawn push: +1.5 points
# For each space a pawn is up from its starting point, 1.5 points will be alotted to the player. Pushing pawns too early
# can be disadvantageous and lead to several hanging pawns, but moving pawns up is one of the central game mechanics and
# pawn positioning in late-game board states is very often the difference between who wins and who loses.

# Covering open squares: +0.15 points
# Each open square that is covered by the player nets 0.15 points. This reinforces the "control the center" mentality and
# incentivizes the AI to wrest control of as much of the board as possible. It is difficult to find a great spot for this
# value though, as it can potentially lead to odd queen moves at the beginning of the game that cover many squares but
# otherwise have no reasonable, immediate impact on the board.
    def eval_board(self, opponent, board):
        score = 0
        # Stale/Checkmate evaluation:
        res = self._logic.safe_check_mate(opponent, self)
        if res == "CM": return float("inf")
        if res == "SM": return 0
        res = self._logic.safe_check_mate(self, opponent)
        if res == "CM": return float("-inf")
        if res == "SM": return 0
        my_pieces = self.get_owned()
        opp_pieces = opponent.get_owned()
        # list of all of the verified legal tiles the players' pieces can move to
        my_legal = self._logic.get_true_legal_player(self, opponent)
        opp_legal = self._logic.get_true_legal_player(opponent, self)
        # Returns a list of all of the squares covered by the pieces, whether it is a legal move or not
        my_covered = self._logic.get_legal_player(self)
        opp_covered = self._logic.get_legal_player(opponent)
        # Lists of the player's and opponent's attacked pieces respectively
        my_attacked = []
        opp_attacked = []
        for coords in my_covered:
            tile = board.get_tile(coords)
            if tile.get_piece() == None: score += 0.15
            elif tile.get_piece().get_type() % 2 == self.get_id():
                score += [0, 0, 50, 30, 32, 15][tile.get_piece().get_type() // 2] * 0.5
            else:
                opp_attacked.append(tile.get_piece())
        for piece in my_pieces:
            type = piece.get_type() // 2
            score += [0, 90, 50, 30, 32, 10][type]
            if 2 <= piece.get_coords()[0] <= 5 and 2 <= piece.get_coords()[1] <= 5: score += 2
            if piece.get_type() == 10: score += (piece.get_coords()[1] - 1) * 1.5
            if piece.get_type() == 11: score += (6 - piece.get_coords()[1]) * 1.5
        for piece in opp_attacked:
            type = piece.get_type() // 2
            if piece.get_coords() in opp_covered: score += [30, 270, 50, 30, 32, 10][type] * 0.2
            else: score += [7.5, 90, 50, 30, 32, 10][type] * 0.8
        for coords in opp_covered:
            tile = board.get_tile(coords)
            if tile.get_piece() == None: score -= 0.15
            elif tile.get_piece().get_type() % 2 == opponent.get_id():
                score -= [0, 0, 50, 30, 32, 15][tile.get_piece().get_type() // 2] * 0.5
            else:
                my_attacked.append(tile.get_piece())
        for piece in opp_pieces:
            type = piece.get_type() // 2
            score -= [0, 90, 50, 30, 32, 10][type]
            if 2 <= piece.get_coords()[0] <= 5 and 2 <= piece.get_coords()[1] <= 5: score -= 2
            if piece.get_type() == 10: score -= (piece.get_coords()[1] - 1) * 1.5
            if piece.get_type() == 11: score -= (6 - piece.get_coords()[1]) * 1.5
        for piece in my_attacked:
            type = piece.get_type() // 2
            if piece.get_coords() in my_covered: score -= [30, 270, 50, 30, 32, 10][type] * 0.2
            else: score -= [7.5, 90, 50, 30, 32, 10][type] * 0.8
        return score

    def randmove(self, opponent, board):
        moves = []
        for piece in self.get_owned():
            piece_coords = piece.get_coords()
            for coords in self._logic.get_true_legal_piece(piece, self, opponent):
                moves.append((piece_coords, coords))
        return moves[randint(0, len(moves) - 1)]

# Alpha-Beta Pruning is a more complex form of minimaxing that can disregard branches in the move tree that are known to
# be obsolete, either by showing the opponent has a worse outcome down the tree or that you will have a better outcome
# down the tree. It always plays in expectation that the opponent will make the moves that benefit you the least and
# continues to make the best possible move based on that scenario.

# In this function, depth represents the total number of turns the function is set to traverse in the turn tree. If
# depth is equal to three on the first call, the AI will search for the best minimum value move within three turns and
# return the most valuable move found from those turns.

# maximizing is a boolean that represents whether or not it is evaluating for the AI or the player. When evaluating for the
# AI, maximizing is set to True and the function will search for the highest score possible the AI can get in the immediate
# turn. If maximizing is set to False, it is the opponent's turn, and the AI will search for the highest score play for the
# opponent, in other words, the score that lowers the AI's score the most. This evaluation method assumes that the
# opponent will always take the best line of play, so it could potentially actually be better in a vacuum at playing
# skilled opponents more so than opponents that make a lot of mistakes/blunders.

# alpha_beta are the max score value and min score values found respectively. Alpha represents the highest score the AI
# has found at the end of its search and Beta represents the lowest score found for the AI that the opponent has made.
# alpha_beta will be stored in a two element list. Alpha starts at -infinity and beta starts at +infinity.
    def alpha_beta_prune(self, opponent, board, depth, maximizing, alpha_beta):
        return
        if depth == 0 or maximizing and self._logic.safe_check_mate(self, opponent) != "NM" or\
            not maximizing and self._logic.safe_check_mate(opponent, self) != "NM":
            return self.eval_board(opponent, board)




