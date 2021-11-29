#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hangman.game import Game


class Defaults:
    WIDTH = 640
    HEIGHT = 400
    STAT_FILE = ".stats"


def main():
    game = Game(
        width=Defaults.WIDTH, height=Defaults.HEIGHT, stat_file=Defaults.STAT_FILE
    )
    game.run()


if __name__ == "__main__":
    main()
