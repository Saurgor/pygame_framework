# -*- coding: utf-8 -*-

import pygame


class MainMenuButton(pygame.sprite.DirtySprite):

    def __init__(self, place):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load('data/images/menu_button.png')
        self.rect = self.image.get_rect()
        self.rect.left = 278
        self.move(place)

    def move(self, place):
        self.rect.top = 317 if place == 'up' else 317 + 82
        self.dirty = 1


class Tile(pygame.sprite.DirtySprite):

    def __init__(self, image, position):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def update(self, xmove=0):
        if xmove > 0:
            self.rect.left -= xmove
            self.dirty = 1


class Map(pygame.sprite.Group):

    def collide(self, char):
        char.rect.move_ip(1, 0)
        collision = pygame.sprite.spritecollideany(char, self)
        char.rect.move_ip(-1, 0)

        return collision


class Charactor(pygame.sprite.DirtySprite):

    def __init__(self, name):
        pygame.sprite.DirtySprite.__init__(self)
        image = 'data/images/charactors/%s/small_right.png' % name
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = 200, 450

        self._xvel = 0
        self._yvel = 0
        self._onground = False
        self._direction = 'right'

    def turn(self, direction):
        if self._direction != direction:
            self._direction = direction
            self.image = pygame.transform.flip(self.image, True, False)

    def move(self, left, right, jump, run, tiledmap):
        half = False

        if left:
            self.turn('left')

            # stop at the left edge
            self._xvel = -5 if self.rect.left > 0 else 0

        if right:
            self.turn('right')
            self._xvel = 5

            # move the map at the half
            if self.rect.left > 370 and not tiledmap.collide(self):
                tiledmap.update(self._xvel)
                self._xvel = 0

        if jump:
            # only jump if on the ground
            if self._onground:
                self._yvel -= 10

        if not self._onground:
            # only accelerate with gravity if in the air
            self._yvel += 0.3
            # max falling speed
            if self._yvel > 60:
                self._yvel = 60

        if not(left or right):
            self._xvel = 0

        # increment in x direction
        self.rect.left += self._xvel

        # do x-axis collisions
        self.collide(self._xvel, 0, tiledmap)

        # increment in y direction
        self.rect.top += self._yvel

        # assuming we're in the air
        self._onground = False

        # do y-axis collisions
        self.collide(0, self._yvel, tiledmap)

        self.dirty = 1

    def collide(self, xvel, yvel, tiledmap):
        for tile in tiledmap:
            if pygame.sprite.collide_rect(self, tile):
                if xvel > 0:
                    self.rect.right = tile.rect.left
                if xvel < 0:
                    self.rect.left = tile.rect.right
                if yvel > 0:
                    self.rect.bottom = tile.rect.top
                    self._onground = True
                    self._yvel = 0
                if yvel < 0:
                    self.rect.top = tile.rect.bottom
                    # fall if touch a block with the head
                    self._yvel = 0
