# -*- coding: utf-8 -*-

import entities
import pygame_framework
import helpers
import pygame
import sprites
from pygame.locals import *


MUSIC_LEVEL = 1.0
SOUND_LEVEL = 1.0


class MainState(pygame_framework.AbstractState):

    # Charactors
    charactors = ('aenyhm', 'djlechuck')
    charactor = charactors[0]


class TitleState(MainState):

    def render(self, background):
        background = pygame.image.load('data/images/menu_screen.jpg').convert()
        if MainState.charactor == MainState.charactors[0]:
            button_place = 'up'
        else:
            button_place = 'down'
        self._button = sprites.MainMenuButton(button_place)

        # Music
        pygame.mixer.music.load('data/music/menu_screen.mid')
        pygame.mixer.music.set_volume(MUSIC_LEVEL)
        pygame.mixer.music.play(-1)

        # Sound
        self._start_sound = pygame.mixer.Sound('data/sounds/start_stage.wav')
        self._start_sound.set_volume(SOUND_LEVEL)

        return background, (self._button), False

    def update(self):
        state = self
        gameloop = True
        for event in pygame.event.get():
            if event.type == QUIT:
                gameloop = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameloop = False

                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    self._start_sound.play()
                    pygame.mixer.music.fadeout(1200)
                    state = GameState

                elif event.key == K_UP:
                    self._button.move('up')
                    MainState.charactor = MainState.charactors[0]

                elif event.key == K_DOWN:
                    self._button.move('down')
                    MainState.charactor = MainState.charactors[1]

        return gameloop, state


class GameState(MainState):

    scenery_overworld = entities.Scenery('overworld')
    #scenery_underground = entities.Scenery('underground')
    #scenery_cascade = entities.Scenery('cascade')
    #scenery_castle = entities.Scenery('castle')
    #scenery_water = entities.Scenery('water')

    def render(self, background):
        # Map
        scenery = GameState.scenery_overworld.background
        background = pygame.image.load(scenery).convert()
        tiles = helpers.render_tmx_map('data/maps/tiles.tmx')
        self._tiledmap = sprites.Map(tiles)

        # Charactor
        self._char = sprites.Charactor(MainState.charactor)
        self._left = self._right = self._jump = self._run = False

        # Music
        pygame.mixer.music.load(GameState.scenery_overworld.music)
        pygame.mixer.music.set_volume(MUSIC_LEVEL)
        pygame.mixer.music.play(-1)

        # Sounds
        self._pause_sound = pygame.mixer.Sound('data/sounds/pause.wav')
        self._pause_sound.set_volume(SOUND_LEVEL)
        self._jump_sound = pygame.mixer.Sound('data/sounds/jump.wav')
        self._jump_sound.set_volume(SOUND_LEVEL)

        return background, (self._tiledmap, self._char), False

    def update(self):
        state = self
        gameloop = True
        for event in pygame.event.get():
            if event.type == QUIT:
                gameloop = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._pause_sound.play()
                    pygame.mixer.music.fadeout(600)
                    state = TitleState
                if event.key == K_z:
                    self._jump = True
                if event.key == K_a:
                    self._run = True
                    self._jump_sound.play()
                if event.key == K_LEFT:
                    self._left = True
                if event.key == K_RIGHT:
                    self._right = True

            elif event.type == KEYUP:
                if event.key == K_z:
                    self._jump = False
                if event.key == K_a:
                    self._run = False
                if event.key == K_LEFT:
                    self._left = False
                if event.key == K_RIGHT:
                    self._right = False

        self._char.move(self._left, self._right, self._jump, self._run,
                        self._tiledmap)

        return gameloop, state
