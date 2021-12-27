from hangman.events import *

from hangman.statistics import Statistics
from hangman.menus import Menus
from hangman.gamestate import GameState
from hangman.conditions import *

ALL_CATEGORIES = {Categories.ANIMALS, Categories.BIRDS, Categories.CHEMISTRY, Categories.COUNTRIES, Categories.FOOD,
                  Categories.FRUITS}


class Game:
    """
    Обрабатывает выборы игрока относительно игры
    """

    def __init__(self, width, height, stat_file):
        pg.init()
        pg.display.set_caption("Hangman")

        self._width, self._height = width, height
        self._surface = pg.display.set_mode((self._width, self._height), pg.RESIZABLE)

        self._stats = Statistics(stat_file)
        self._cond = Conditions(
            difficulty=Difficulty.EASY,
            categories=ALL_CATEGORIES,
            cond_hint=False,
            cond_timer=False,
        )
        self._game_state = GameState()
        self._menus = Menus(self._width, self._height, self._cond, self._game_state, self._surface)
        self._running = True

    def on_event(self, event):
        if event.type == pg.QUIT:
            print("on_event(): pg.QUIT")
            self._running = False
        if event.type == pg.VIDEORESIZE:
            print("on_event(): pg.VIDEORESIZE")
            self._surface = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
            self._width, self._height = event.w, event.h
            self._menus.resize(event.w, event.h)
        if event.type == CLEAR_STATS:
            print("on_event(): CLEAR_STATS")
            self._stats.clear()
        if event.type == HINT:
            self._menus.game_state.get_hint()
            print("on_event(): HINT")
        if event.type == CONTINUE:
            print("on_event(): CONTINUE")
            pass
        # TODO: Найти нормальную функцию отрисовки меню, не ломающую функциал кнопок
        if event.type == LOSE:
            print("on_event(): LOSE")
            self._menus.defeat.mainloop(self._surface)
        if event.type == WIN:
            print("on_event(): WIN")
            self._menus.victory.mainloop(self._surface)
        if event.type == START_GAME:
            print("on_event(); START_GAME")
            self._game_state.change_word(self._cond.categories)
            # dev: если нужно будет после смены слова пересоздать игровое меню
            # то можно в классе Menus определить фукнцию, которая при вызове извне бы это делала
            # и вызвать её здесь
            self._menus.game.mainloop(self._surface)

    def run(self):
        while self._running:
            events = pg.event.get()
            for event in events:
                self.on_event(event)

            if self._menus.main.is_enabled():
                self._menus.main.update(events)
                self._menus.main.draw(self._surface)
            pg.display.update()
