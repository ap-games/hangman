import pygame_menu as pgm

from hangman.events import *
from hangman.gamestat import *


class Menus:
    """
    Создает и хранит в себе игровые меню
    """

    # TODO: Допилить менюшки

    def __init__(self, width: int, height: int):
        self._height = height
        self._width = width
        self.cursor = pgm.locals.CURSOR_HAND
        self.game_state = GameState()
        self.victory = self._create_victory()
        self.defeat = self._create_defeat()
        self.game = self._create_game(self.game_state)
        self.stats = self._create_stats()
        self.settings = self._create_settings(self.game)
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
        stat.add.button("Сбросить", post_clear_stats)
        print("Stats")
        return stat

    def _create_settings(self, game):
        settings = pgm.menu.Menu(
            title="Настройки", height=self._height, width=self._width
        )
        settings.add.button("Назад", pgm.events.BACK)
        settings.add.button("Продолжить", game)
        return settings

    def _create_main(self, settings, stats):
        main = pgm.menu.Menu(title="Hangman", height=self._height, width=self._width)
        main.add.button("Играть", settings)
        main.add.button("Статистика", stats, accept_kwargs=True)
        main.add.button("Выйти", pgm.events.EXIT)
        return main

    def _create_game(self, game_state):
        game = pgm.menu.Menu(title="Hangman", height=self._height, width=self._width)
        alphabet = [
            "А", "Б", "В", "Г", "Д", "Е", "Ж", "И", "Й", "К", "Л", "М", "Н", "О",
            "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь",
            "Э", "Ю", "Я"
        ]

        buttons = lambda x: game.add.button(
            x, lambda: self.game_state.update_state(x), cursor=self.cursor
        )
        [buttons(letter) for letter in alphabet]

        # # WIP
        # [buttons(letter) for letter in alphabet]
        # button = game.add.button(letter, game_state.update_state(letter))
        # button.set_position(50.0, 800.0)
        # button.set_position()
        b = game.add.button("тест", pgm.events.NONE)
        # b.set_col_row_index(10, 100, 10)
        # b.set_position(10.0,200.0)

        back = game.add.button("Назад", pgm.events.BACK)
        return game

    # TODO: доделать кнопки
    def _create_victory(self):
        victory = pgm.menu.Menu(
            title="Вы выиграли!", height=self._height, width=self._width
        )
        victory.add.button("Назад", pgm.events.BACK)
        print("_create_victory(self)")
        return victory

    def _create_defeat(self):
        defeat = pgm.menu.Menu(
            title="Вы проиграли!", height=self._height, width=self._width
        )
        defeat.add.button("Назад", pgm.events.BACK)
        print("_create_defeat(self)")
        return defeat
