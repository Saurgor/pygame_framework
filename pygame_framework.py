# -*- coding: utf-8 -*-

"""
pygame_framework
~~~~~~~~~~~~~~~~

This module helps making a game in Python with Pygame.

:copyright: (c) 2013 by Fabien Nouaillat.
:license: MIT, see LICENSE for more details.

"""

import abc
import pygame


class AbstractState(object):
    """Superclass of any state in the game."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, app):
        self._app = app

    def render(self, background):
        allsprites = ()
        mouse = False

        return background, allsprites, mouse

    def update(self):
        gameloop = True
        state = self
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                gameloop = False

        return gameloop, state


class AbstractStateMachine(object):
    """Manage the states of the game."""

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._states = []
        self._active_state = None

    def add_state(self, state, mouse=False):
        if not self.has_state(state):
            if issubclass(state, AbstractState):
                self._states.append(state)
            else:
                raise Exception(
                    ("The state `{}` must inherits AbstractState.").format(
                        state))
        else:
            raise Exception(
                ("The state `{}` has already been added.").format(state))

    def enter_state(self, state):
        if state in self._states:
            self._active_state = state(self)
        else:
            raise Exception(("The state `{}` cannot be found.").format(state))

    def has_state(self, state):
        return state in self._states


class AbstractGame(AbstractStateMachine):
    """A class which avoids rewriting the basic Pygame mechanics."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, title, size, fps=60):
        AbstractStateMachine.__init__(self)
        pygame.init()
        self._screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self._clock = pygame.time.Clock()
        self._fps = fps

    def _render(self):
        # Create the backgound
        self._background = pygame.Surface(self._screen.get_size())
        self._background = self._background.convert()
        self._background.fill((250, 250, 250))
        self._background, sprites, mouse = self._active_state.render(
            self._background)

        # Show the mouse
        pygame.mouse.set_visible(mouse)

        # Display the background
        self._screen.blit(self._background, (0, 0))
        pygame.display.flip()

        # Prepare game objects
        self._allsprites = pygame.sprite.LayeredDirty(sprites)
        self._allsprites.clear(self._screen, self._background)

    def start(self):
        self._render()
        running = True
        while running:
            # Set FPS
            self._clock.tick(self._fps)

            # Handle events
            running, state = self._active_state.update()

            if running:
                # Manage state changes
                if self._active_state != state:
                    self.enter_state(state)
                    self._render()

                # Update the display
                self._allsprites.update()
                rects = self._allsprites.draw(self._screen)
                pygame.display.update(rects)

        pygame.quit()
