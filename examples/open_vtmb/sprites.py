# -*- coding: utf-8 -*-

import abc
import pygame


class AbstractWidget(pygame.sprite.DirtySprite):
    """Base class of GUI elements."""

    __metaclass__ = abc.ABCMeta


class TextLabel(AbstractWidget):

    def __init__(self, text, antialias=True):
        self._text = text
        self._antialias = antialias
        self._properties = {}
        self._font = None
        self._final_text = None

    def stylize(self, **kwargs):
        self._properties.update(kwargs)

    def render(self):
        self._font = pygame.font.Font(self._properties['font_family'],
                                      self._properties['font_size'])

        self._final_text = self._font.render(self._text,
                                             self._antialias,
                                             self._properties['color'])

        return self._final_text

    def get_rect(self, background):
        if self._properties['text_align'] == 'center':
            centerx = background.get_width() / 2
        else:
            centerx = self._properties['margin_left']

        centery = self._properties['margin_top']

        return self._final_text.get_rect(centerx=centerx, centery=centery)

    def hover(self):
        if self._properties['text_underline_hover']:
            self._font = font.set_underline()


class LinkToState(object):

    def __init__(self, state, title, rect=None):
        self._rect = rect
        self._state = state
        self._title = title

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    @property
    def state(self):
        return self._state if self._state != -1 else None

    @property
    def title(self):
        return self._title

    def is_mouse_over(self):
        xmouse, ymouse = pygame.mouse.get_pos()

        xmouse_over = xmouse >= self._rect.left and xmouse <= self._rect.right
        ymouse_over = ymouse >= self._rect.top and ymouse <= self._rect.bottom

        return xmouse_over and ymouse_over
