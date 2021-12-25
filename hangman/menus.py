import pygame_menu as pgm

from hangman.events import *
from hangman.gamestate import *
from hangman.conditions import *

class Menus:
    """
    Создает и хранит в себе игровые меню
    """

    # TODO: Допилить менюшки

    def __init__(self, width: int, height: int, cond: Conditions, game_state: GameState, surface: any):
        self._height = height
        self._width = width
        self._surface = surface
        self.cond = cond
        self.game_state = game_state
        self.cursor = pgm.locals.CURSOR_HAND
        self.victory = self._create_victory()
        self.defeat = self._create_defeat()
        # self.game = self._create_game(self.game_state)
        self.stats = self._create_stats()
        self.settings, self.game = self._create_settings(self.cond)
        self.main = self._create_main(self.settings, self.stats)

    def resize(self, width: int, height: int):
        # Подумать: Можно попробовать сократить код, засунув все менюшки в словарь, и обходом по словарю вызывать .resize(). С другой стороны не так уж и много у нас менюшек.
        # Подумать: Возможно неплохо было бы ресайзить только текущее показываемое окно, но тогда нужно будет понять, как узнавать, какое окно сейчас показывается, а так же не забывать ресайзить при переходах между менюшками и их. Звучит довольно запарно. Учитывая, что менюшек у нас не так много, возможно хорошей идеей будет оставить как есть.

        # TODO: проверить чтобы все меню ресайзились, и все были учтены здесь при добавлении кода
        print("resize()")
        self._width, self._height = width, height
        self.main.resize(width, height)
        self.stats.resize(width, height)
        self.settings.resize(width, height)
        self.victory.resize(width, height)
        self.defeat.resize(width, height)
        self.game.resize(width, height)

    def _create_stats(self):
        stat = pgm.menu.Menu(title="Статистика", height=self._height, width=self._width)
        stat.add.button("Назад", pgm.events.BACK)
        stat.add.button("Сбросить", post_lost(CLEAR_STATS))
        print("Stats")
        return stat

    def _create_settings(self, cond):
        settings = pgm.menu.Menu(
            title="Настройки", height=self._height, width=self._width
        )

        print(self.cond.hint)
        self.cond.set_cond_hint(True)
        print(self.cond.hint)

        game = self._create_game(self.game_state)

        settings.add.button("Продолжить", game)
        settings.add.button("Назад", pgm.events.BACK)

        return settings, game

    def _create_main(self, settings, stats):
        main = pgm.menu.Menu(title="Hangman", height=self._height, width=self._width)
        main.add.button("Играть", settings)
        main.add.button("Статистика", stats, accept_kwargs=True)
        main.add.button("Выйти", pgm.events.EXIT)
        return main

    def _create_game(self, game_state):
        game = pgm.menu.Menu(title="Hangman", height=self._height, width=self._width)

        buttons = lambda x: game.add.button(
            x, lambda: self.game_state.update_state(x), cursor=self.cursor
        )
        for letter in ALPHABET:
            buttons(letter)
        # # WIP
        # [buttons(letter) for letter in alphabet]
        # button = game.add.button(letter, game_state.update_state(letter))
        # button.set_position(50.0, 800.0)
        # button.set_position()
        # b = game.add.button("тест", pgm.events.NONE)
        # b.set_col_row_index(10, 100, 10)
        # b.set_position(10.0,200.0)

        self._add_hint_button(game, self.cond.hint)
        game.add.button("Назад", pgm.events.BACK)
        return game

    def _add_hint_button(self, game, hint):
        print(f"In add_but: {hint}")
        if hint == False:
            return

        game.add.button("Подсказка", post_lost(HINT))
        return

    # TODO: доделать кнопки
    def _create_victory(self):
        victory = pgm.menu.Menu(
            title="Вы выиграли!", height=self._height, width=self._width
        )
        victory.add.button("Назад", pgm.events.PYGAME_QUIT)
        print("_create_victory(self)")
        return victory

    def _create_defeat(self):
        defeat = pgm.menu.Menu(
            title="Вы проиграли!", height=self._height, width=self._width
        )
        defeat.add.button("Назад", post_lost(CLEAR_STATS))
        defeat.add.button("Назад", pgm.events.PYGAME_QUIT)
        print("_create_defeat(self)")
        return defeat