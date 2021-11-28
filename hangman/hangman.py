#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame as pg
import pygame_menu as pgm


class GameState:
    """
    Хранит текущее состояние игры
    """

    # TODO: Реализовать
    def __init__(self):
        pass


class Menus:
    """
    Создает и хранит в себе игровые меню
    """

    # TODO: Допилить менюшки

    def __init__(self, width: int, height: int):
        self._height = height
        self._width = width

        self.stats = self._create_stats()
        self.settings = self._create_settings()
        self.main = self._create_main(self.settings, self.stats)
        self.victory = self._create_victory()
        self.defeat = self._create_defeat()
        self.game = self._create_game()

    def resize(self, width: int, height: int):
        # Подумать: Можно попробовать сократить код, засунув все менюшки в словарь, и обходом по словарю вызывать .resize(). С другой стороны не так уж и много у нас менюшек.

        # Подумать: Возможно неплохо было бы ресайзить только текущее показываемое окно, но тогда нужно будет понять, как узнавать, какое окно сейчас показывается, а так же не забывать ресайзить при переходах между менюшками и их. Звучит довольно запарно. Учитывая, что менюшек у нас не так много, возможно хорошей идеей будет оставить как есть.

        print("resize()")
        self._width, self._height = width, height
        self.main.resize(width, height)
        self.stats.resize(width, height)
        self.settings.resize(width, height)
        # self.victory.resize(width, height)
        # self.defeat.resize(width, height)
        # self.game.resize(width, height)

    def _create_stats(self):
        stat = pgm.menu.Menu(title="Hangman", height=self._height, width=self._width)
        stat.add.button("Назад", pgm.events.BACK)
        return stat

    def _create_settings(self):
        settings = pgm.menu.Menu(
            title="Hangman", height=self._height, width=self._width
        )
        settings.add.button("Назад", pgm.events.BACK)
        return settings

    def _create_main(self, settings, stats):
        main = pgm.menu.Menu(title="Hangman", height=self._height, width=self._width)
        main.add.button("Играть", settings)
        main.add.button("Статистика", stats)
        main.add.button("Выйти", pgm.events.EXIT)
        return main

    def _create_game(self):
        return None

    def _create_victory(self):
        return None

    def _create_defeat(self):
        return None


class Game:
    """
    Обрабатывает выборы игрока относительно игры
    """

    # TODO: Допилить
    def __init__(self):
        pg.init()
        pg.display.set_caption("Hangman")
        self._size = self._width, self._height = 640, 400
        self._surface = pg.display.set_mode(self._size, pg.RESIZABLE)
        self._menus = Menus(self._width, self._height)
        self._running = True

    def on_event(self, event):
        if event.type == pg.QUIT:
            print("on_event(): pg.QUIT")
            self._running = False
        if event.type == pg.VIDEORESIZE:
            print("on_event(): pg.VIDEORESIZE")
            self._surface = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            self._size = self._width, self._height = event.w, event.h
            self._menus.resize(event.w, event.h)

    def run(self):
        while self._running:
            events = pg.event.get()
            for event in events:
                self.on_event(event)

            if self._menus.main.is_enabled():
                self._menus.main.update(events)
                self._menus.main.draw(self._surface)

            pg.display.update()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
