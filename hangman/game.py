import pygame as pg

from hangman.events import *
import pygame_menu as pgm
import datetime
from hangman.statistics import Statistics
from hangman.menus import Menus
from hangman.gamestate import GameState
from hangman.conditions import *

class Game:
    """
    Обрабатывает выборы игрока относительно игры
    """

    def __init__(self, width, height, stat_file):
        pg.init()
        pg.display.set_caption("Hangman")
        self._width, self._height = width, height
        self._surface = pg.display.set_mode((self._width, self._height), pg.RESIZABLE)

        self._game_state = GameState()
        self._stats = Statistics(stat_file)
        self._cond = Conditions(
            difficulty=Difficulty.EASY,
            categories=ALL_CATEGORIES,
            cond_hint=False,
            cond_timer=False,
        )

        self._menus = Menus(
            width=self._width,
            height=self._height,
            conds=self._cond,
            game_state=self._game_state,
            stats=self._stats,
        )
        self._current_menu = self._menus.main
        self._running = True

    def on_event(self, event):
        if event.type == pg.QUIT:
            print("[dbg] on_event(): pg.QUIT")
            self._stats.write_stats()
            self._running = False

        elif event.type == pg.VIDEORESIZE:
            print("[dbg] on_event(): pg.VIDEORESIZE")
            self._surface = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            self._width, self._height = event.w, event.h
            self._menus.resize(event.w, event.h)

        elif event.type == CLEAR_STATS:
            print("[dbg] on_event(): CLEAR_STATS")
            self._stats.clear()

        elif event.type == HINT:
            self._menus.game_state.get_hint()

            print("[dbg] on_event(): HINT")

        elif event.type == CONTINUE:
            print("[dbg] on_event(): CONTINUE")

        elif event.type == LOSE:
            print("[dbg] on_event(): LOSE")
            self._stats.played += 1
            self._current_menu = self._menus.defeat

        elif event.type == WIN:
            self._stats.played += 1
            self._stats.won += 1
            print("[dbg] on_event(): WIN")
            self._current_menu = self._menus.victory

        elif event.type == START_GAME:
            print("[dbg] on_event(); START_GAME")

            self._game_state.change_word(self._cond.categories)
            # TODO: если нужно будет после смены слова пересоздать игровое меню
            # то можно в классе Menus определить фукнцию, которая при вызове извне бы это делала

            self._current_menu = self._menus.game

        elif event.type == BACK_TO_MAIN:
            print("[dbg] on_event(); BACK_FROM_*")
            self._current_menu = self._menus.main


    def run(self):
        # FIXME! WIP!
        clock = pg.time.Clock()
        global timer
        timer = [0]
        dt = 1.0 / FPS
        timer_font = pgm.font.get_font(pgm.font.FONT_NEVIS, 100)
        frame = 0

        while self._running:
            events = pg.event.get()
            for event in events:
                self.on_event(event)

            if self._running:
                self._current_menu.update(events)
                self._current_menu.draw(self._surface)

            pg.display.update()
