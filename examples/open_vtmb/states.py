# -*- coding: utf-8 -*-

import collections
from framework import AbstractState
import pygame
from pygame.locals import *
from sprites import LinkToState as lts, TextLabel


class TitleState(AbstractState):

    def render(self, background):
        background.fill((0, 0, 0))

        typo = 'data/fonts/vrev.ttf'

        # Title
        title = TextLabel("Vampire")
        title.stylize(color=(218, 197, 107),
                      font_family=typo,
                      font_size=92,
                      margin_top=80,
                      text_align='center')
        background.blit(title.render(), title.get_rect(background))

        # Subtitle
        subtitle = TextLabel("The Masquerade")
        subtitle.stylize(color=(172, 136, 105),
                         font_family=typo,
                         font_size=48,
                         margin_top=140,
                         text_align='center')
        background.blit(subtitle.render(), subtitle.get_rect(background))

        # Menu
        self._menu = (lts(GameState, "Nouvelle partie"),
                      lts(-1, "Charger partie"),
                      lts(QuitState, "Quitter"))

        margintop = 250

        for item in self._menu:
            menu_item = TextLabel(item.title)
            menu_item.stylize(color=(153, 0, 3),
                              font_family=typo,
                              font_size=36,
                              margin_top=margintop,
                              text_align='center',
                              text_underline_hover=True)
            item_render = menu_item.render()
            item_rect = menu_item.get_rect(background)
            background.blit(item_render, item_rect)
            item.rect = item_rect
            margintop += 60

        return background, (), True

    def update(self):
        gameloop = True
        state = self

        for event in pygame.event.get():
            if event.type == QUIT:
                gameloop = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameloop = False

            elif event.type == MOUSEMOTION:
                for item in self._menu:
                    if item.is_mouse_over():
                        pass #item.hover()

            elif event.type == MOUSEBUTTONDOWN:
                for item in self._menu:
                    if item.is_mouse_over():
                        if self._app.has_state(item.state):
                            state = item.state

        return gameloop, state


class GameState(AbstractState):

    def render(self, background):
        background.fill((0, 0, 0))

        # Temporary message
        font = pygame.font.Font(None, 36)
        msg = font.render("Game is coming!", 1, (220, 220, 220))
        msg_rect = msg.get_rect(centerx=background.get_width() / 2,
                                centery=background.get_height() / 2)
        background.blit(msg, msg_rect)

        return background, (), False

    def update(self):
        gameloop = True
        state = self

        for event in pygame.event.get():
            if event.type == QUIT:
                gameloop = False

            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                state = TitleState

        return gameloop, state


class QuitState(AbstractState):

    def update(self):
        return False, self
