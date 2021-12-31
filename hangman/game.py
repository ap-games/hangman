import pygame as pg

from hangman.events import *

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
        size = self._width, self._height = width, height
        self._surface = pg.display.set_mode(size, pg.RESIZABLE)

        self._game_state = GameState()
        self._stats = Statistics(stat_file)
        self._cond = Conditions(
            difficulty=Difficulty.EASY,
            categories=set(ALL_CATEGORIES),
            has_hint=True,
            has_timer=True,
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
            self._running = False

        elif event.type == pg.VIDEORESIZE:
            print("[dbg] on_event(): pg.VIDEORESIZE")
            size = event.w, event.h
            self._surface = pg.display.set_mode(size, pg.RESIZABLE)
            self._width, self._height = event.w, event.h
            self._menus.resize(event.w, event.h)

        elif event.type == CLEAR_STATS:
            print("[dbg] on_event(): CLEAR_STATS")
            self._stats.clear()
            self._menus.update_stats(self._stats)

        elif event.type == HINT:
            print("[dbg] on_event(): HINT")
            self._game_state.get_hint()
            self._menus.hide_hint()

        elif event.type == CONTINUE:
            print("[dbg] on_event(): CONTINUE")

        elif event.type == LOSE:
            print("[dbg] on_event(): LOSE")
            self._stats.played += 1
            self._menus.update_stats(self._stats)
            self._current_menu = self._menus.defeat

        elif event.type == WIN:
            self._stats.played += 1
            self._stats.won += 1
            self._menus.update_stats(self._stats)
            print("[dbg] on_event(): WIN")
            self._current_menu = self._menus.victory

        elif event.type == START_GAME:
            print("[dbg] on_event(); START_GAME")
            self._game_state.new_game(self._cond)
            self._menus.setup_game(self._cond, self._game_state)
            self._current_menu = self._menus.game

        elif event.type == BACK_TO_MAIN:
            print("[dbg] on_event(); BACK_FROM_*")
            self._current_menu = self._menus.main

        elif event.type == HIDE_HINT:
            print("[dbg]on_event(); HIDE_HINT")
            self._menus.hide_hint()

    def run(self):
        while self._running:
            events = pg.event.get()
            for event in events:
                self.on_event(event)
            
            if self._current_menu == self._menus.game and self._cond.has_timer:
                self._game_state.update_timer()
                self._menus.update_timer(self._game_state.time_left)

            self._current_menu.update(events)
            self._current_menu.draw(self._surface)

            pg.display.update()
