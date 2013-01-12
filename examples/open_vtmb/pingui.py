# -*- coding: utf-8 -*-

import abc
import pygame


class AbstractWidget(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.rect = None

    def is_mouse_over(self):
        xmouse, ymouse = pygame.mouse.get_pos()
        xmouse_over = xmouse >= self.rect.left and xmouse <= self.rect.right
        ymouse_over = ymouse >= self.rect.top and ymouse <= self.rect.bottom

        return xmouse_over and ymouse_over


class Text(AbstractWidget):

    def __init__(self, text):
        AbstractWidget.__init__(self)
        self._text = text
        self._style = {}
        self._font = None
        self._surface = None

    def render_on(self, background):
        self._background = background

    def stylize(self, **kwargs):
        self._style.update(kwargs)

    def _hover(self):
        if self._style['text_underline_hover']:
            self._font.set_underline(True)

    def update(self):
        self._set_font()
        self._set_rect()
        self._background.blit(self._surface, self.rect)

    def _set_font(self):
        self._font = pygame.font.Font(self._style['font_family'],
                                      self._style['font_size'])

        if self.rect and self.is_mouse_over():
            self._hover()
        self._surface = self._font.render(self._text, 1, self._style['color'])

    def _set_rect(self):
        if self._style['text_align'] == 'center':
            centerx = self._background.get_width() / 2
        else:
            centerx = self._style['margin_left']

        centery = self._style['margin_top']

        self.rect = self._surface.get_rect(centerx=centerx, centery=centery)


class Label(Text):
    pass


class LinkToState(Text):

    def __init__(self, text, state=None):
        Text.__init__(self, text)
        self._state = state

    @property
    def state(self):
        return self._state
