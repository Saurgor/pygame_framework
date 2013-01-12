# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from pygame_framework import AbstractGame
from states import TitleState, GameState, QuitState


class App(AbstractGame):

    def __init__(self):
        AbstractGame.__init__(self, "Open VTMB", (800, 600))

        self.add_state(TitleState)
        self.add_state(GameState)
        self.add_state(QuitState)
        self.enter_state(TitleState)


if __name__ == '__main__':
    app = App()
    app.start()
