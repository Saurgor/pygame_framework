# -*- coding: utf-8 -*-

import pygame
from pygame_framework import AbstractState
from pygame.locals import *
from pingui import LinkToState, Label


class TitleState(AbstractState):

    def render(self, background):
        background.fill((0, 0, 0))

        typo = 'data/fonts/vrev.ttf'

        # Title
        title = Label("Vampire")
        title.stylize(color=(218, 197, 107),
                      font_family=typo,
                      font_size=92,
                      margin_top=80,
                      text_align='center')
        title.render_on(background)
        title.update()

        # Subtitle
        subtitle = Label("The Masquerade")
        subtitle.stylize(color=(172, 136, 105),
                         font_family=typo,
                         font_size=48,
                         margin_top=140,
                         text_align='center')
        subtitle.render_on(background)
        subtitle.update()

        # Menu
        self._menu = (LinkToState("Nouvelle partie", GameState),
                      LinkToState("Charger partie"),
                      LinkToState("Quitter", QuitState))

        margintop = 250

        menu_sprites = []
        for item in self._menu:
            item.stylize(color=(153, 0, 3),
                         font_family=typo,
                         font_size=36,
                         margin_top=margintop,
                         text_align='center',
                         text_underline_hover=True)
            item.render_on(background)
            item.update()
            menu_sprites.append(item)
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
                        item.update()  # KO

            elif event.type == MOUSEBUTTONDOWN:
                for item in self._menu:
                    if item.is_mouse_over():
                        if item.state:
                            if self._app.has_state(item.state):
                                state = item.state
                            else:
                                raise Exception(
                                    ("The state `{}` cannot be found.").format(
                                        state))

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
