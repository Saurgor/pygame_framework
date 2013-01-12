# -*- coding: utf-8 -*-


class Scenery(object):

    def __init__(self, resource):
        self._background = 'data/images/backgrounds/%s.jpg' % resource
        self._music = 'data/music/%s.mid' % resource

    @property
    def background(self):
        return self._background

    @property
    def music(self):
        return self._music
