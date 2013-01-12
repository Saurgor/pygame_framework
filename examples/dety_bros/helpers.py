# -*- coding: utf-8 -*-

import sprites
import pytmx


def render_tmx_map(tmx_file):
    tiledmap = pytmx.tmxloader.load_pygame(tmx_file, pixelalpha=True)

    tw = tiledmap.tilewidth
    th = tiledmap.tileheight
    gt = tiledmap.getTileImage

    tiles = []

    for l in xrange(0, len(tiledmap.tilelayers)):
        for y in xrange(0, tiledmap.height):
            for x in xrange(0, tiledmap.width):
                tile = gt(x, y, l)
                if tile:
                    tiles.append(sprites.Tile(tile, (x * tw, y * th)))

    return tiles
