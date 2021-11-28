#!/usr/bin/env python3

import pygame as pg
import pygame_menu as pgm


class GameState:
    """
    Хранит текущее состояние игры
    """

    # TODO: Реализовать
    def __init__(self):
        pass


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

        self._stat_menu = pgm.menu.Menu(
            title="Hangman", height=self._height, width=self._width
        )
        self._stat_menu.add.button("Back", pgm.events.BACK)

        self._menu = pgm.menu.Menu(
            title="Hangman", height=self._height, width=self._width
        )
        self._menu.add.button("Play", self._stat_menu)
        self._menu.add.button("Quit", pgm.events.EXIT)

        self._running = True

    def on_event(self, event):
        if event.type == pg.QUIT:
            print("on_event(): pg.QUIT")
            self._running = False
        if event.type == pg.VIDEORESIZE:
            print("on_event(): pg.VIDEORESIZE")
            self._surface = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            self.on_resize()

    @staticmethod
    def cleanup():
        print("cleanup()")
        pg.quit()

    def on_resize(self) -> None:
        print("on_resize()")
        self._size = self._width, self._height = self._surface.get_size()
        self._menu.resize(self._width, self._height)

    def run(self):
        while self._running:
            events = pg.event.get()
            for event in events:
                self.on_event(event)

            if self._menu.is_enabled():
                self._menu.update(events)
                self._menu.draw(self._surface)

            pg.display.update()
        self.cleanup()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
