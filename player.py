import pygame
from piece import *

# Class that represents a player and the pieces they own/have captured
class Player:
    def __init__(self, pid, board):
        self._pid = pid
        self._score = 0
        self._captures = [0, 0, 0, 0, 0]  # [Q, R, N, B, P]
        self._owned_pieces = pygame.sprite.Group()

    def get_id(self):
        return self._pid

    def get_owned(self):
        return self._owned_pieces

    def get_captures(self):
        return self._captures

    def get_king(self):
        return self._king

    def record_capture(self, capture):
        self._captures[capture] += 1
        if capture == 0: # Queen capture
            self._score += 9
        if capture == 1: # Rook capture
            self._score += 5
        if capture == 2 or capture == 3: # Knight or Bishop capture
            self._score += 3
        if capture == 4: # Pawn capture
            self._score += 1