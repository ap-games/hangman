import pygame as pg

from hangman.helpers import dbg_log
from hangman.events import *

from hangman.statistics import Statistics
from hangman.menus import Menus
from hangman.gamestate import GameState
from hangman.conditions import Conditions, Difficulties, ALL_CATEGORIES


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
        self._conditions = Conditions(
            difficulty=Difficulties["EASY"],
            categories=set(ALL_CATEGORIES),
            has_hint=True,
            has_timer=True,
        )
        self._menus = Menus(
            width=self._width,
            height=self._height,
            conditions=self._conditions,
            stats=self._stats,
        )
        self._current_menu = self._menus.main
        self._running = True

    def on_event(self, event):
        if event.type == pg.QUIT:
            dbg_log("on_event(): pg.QUIT")
            self._running = False

        elif event.type == pg.VIDEORESIZE:
            dbg_log("on_event(): pg.VIDEORESIZE")
            size = event.w, event.h
            self._surface = pg.display.set_mode(size, pg.RESIZABLE)
            self._width, self._height = event.w, event.h
            self._menus.resize(event.w, event.h)

        elif event.type == CLEAR_STATS:
            dbg_log("on_event(): CLEAR_STATS")
            self._stats.clear()
            self._menus.update_stats(self._stats)

        elif event.type == HINT:
            dbg_log("on_event(): HINT")
            self._menus.show_hint(self._game_state)
            self._menus.hide_hint_button()

        elif event.type == PAUSE:
            dbg_log("on_event(): PAUSE")
            self._current_menu = self._menus.pause

        elif event.type == CONTINUE:
            dbg_log("on_event(): CONTINUE")
            self._game_state.unpause()
            self._current_menu = self._menus.game

        elif event.type == WRONG_GUESS:
            dbg_log(f"on_event(): DRAW_GALLOWS")
            self._menus.update_gallows(self._game_state.lifes)

        elif event.type == LOSE:
            dbg_log("on_event(): LOSE")
            self._stats.played += 1
            self._menus.update_stats(self._stats)
            self._current_menu = self._menus.defeat

        elif event.type == WIN:
            dbg_log("on_event(): WIN")
            self._stats.played += 1
            self._stats.won += 1
            self._menus.update_stats(self._stats)
            self._current_menu = self._menus.victory

        elif event.type == START_GAME:
            dbg_log("on_event(): START_GAME")
            self._game_state.new_game(self._conditions)
            self._menus.setup_game(self._conditions, self._game_state.word)
            self._current_menu = self._menus.game

        elif event.type == BACK_TO_MAIN:
            dbg_log("on_event(): BACK_TO_MAIN")
            self._current_menu = self._menus.main

        elif event.type == HIDE_HINT:
            dbg_log("on_event(): HIDE_HINT")
            self._menus.hide_hint_button()

        elif event.type == LETTER_CHOSEN:
            dbg_log(f"on_event(): LETTER_CHOSEN {event.letter}")
            self._game_state.process_letter(event.letter)
            self._menus.reveal_letter(event.letter)
            self._menus.block_letter(event.letter)

        elif event.type == CHANGE_CONDITIONS:
            dbg_log("on_event(): CHANGE_CONDITIONS")
            action = event.action
            value = event.value
            self._conditions.handle_action(action, value)

        elif event.type == BLOCK_START:
            dbg_log("on_event(): BLOCK_START")
            self._menus.block_start()

        elif event.type == ALLOW_START:
            dbg_log("on_event(): ALLOW_START")
            self._menus.allow_start()

        elif event.type == SURRENDER:
            dbg_log("on_event(): SURRENDER")
            self._stats.played += 1
            self._menus.update_stats(self._stats)
            post_back_to_main()

    def run(self):
        clock = pg.time.Clock()

        while self._running:
            events = pg.event.get()
            for event in events:
                self.on_event(event)

            if self._current_menu == self._menus.game and self._conditions.has_timer:
                self._game_state.update_timer()
                self._menus.update_timer(self._game_state.time_left)

            self._current_menu.update(events)
            self._current_menu.draw(self._surface)

            pg.display.update()
            clock.tick(30)
