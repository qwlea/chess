import pygame

# Class that handles creating text objects to be displayed on the screen
class Text:
    def __init__(self, font, text, txt_color, bg_color, x, y):
        self._text = font.render(text, True, txt_color, bg_color)
        self._rect = self._text.get_rect()
        self._rect.x = x
        self._rect.y = y
        self._font = font
        self._txt_c = txt_color
        self._bg_c = bg_color

    # Displays the text by "pasting" it onto the given surface with the blit method
    def paste(self, surface):
        surface.blit(self._text, self._rect)

    def updateText(self, new_text):
        self._text = self._font.render(new_text, True, self._txt_c, self._bg_c)
        tmp_x = self._rect.x
        tmp_y = self._rext.y
        self._rect = self._text.get_rect()
        self._rect.x = tmp_x
        self._rect.y = tmp_y