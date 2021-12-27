import pygame_menu as pgm
from typing import Tuple
from hangman.events import *
from hangman.gamestate import *
from hangman.conditions import *


class Menus:
    """
    Создает и хранит в себе игровые меню
    """

    # TODO: Допилить менюшки

    def __init__(self, width: int, height: int, conds: Conditions, game_state: GameState, surface: any):
        self._height = height
        self._width = width
        self._surface = surface
        self.cursor = pgm.locals.CURSOR_HAND
        
        self.game_state = game_state
        self.cond = conds

        self.victory = self._create_victory()
        self.defeat = self._create_defeat()
        self.stats = self._create_stats()
        self.game = self._create_game(self.game_state)
        self.settings = self._create_settings(conds)
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

    def _change_difficulty(self, value: Tuple[any, int], difficulty: str) -> None:
        selected, index = value
        print(f'Selected difficulty: "{selected}" ({difficulty}) at index {index}')
        self.cond.set_difficulty(index + 1)

    def _change_hint(self, value: Tuple, enabled: bool) -> None:
        if enabled:
            self.cond.set_cond_hint(True)
        else:
            self.cond.set_cond_hint(False)
        print(f'Hint is available: {self.cond.hint}')

    def _change_timer(self, value: Tuple, enabled: bool) -> None:
        if enabled:
            self.cond.set_cond_timer(True)
        else:
            self.cond.set_cond_timer(False)
        print(f'Timer: {self.cond.timer}')

    def _change_category(self, value: Tuple, enabled: str) -> None:
        selected, index = value
        if enabled == 'ALL':
            self.cond.add_category(1)
            self.cond.add_category(2)
            self.cond.add_category(3)
            self.cond.add_category(4)
            self.cond.add_category(5)
            self.cond.add_category(6)
        elif enabled == 'NONE':
            self.cond.categories.clear()
        elif enabled == 'ANIMALS':
            self.cond.add_category(1)
        elif enabled == 'NOT_ANIMALS':
            self.cond.delete_category(1)
        elif enabled == 'BIRDS':
            self.cond.add_category(2)
        elif enabled == 'NOT_BIRDS':
            self.cond.delete_category(2)
        elif enabled == 'CHEMISTRY':
            self.cond.add_category(3)
        elif enabled == 'NOT_CHEMISTRY':
            self.cond.delete_category(3)
        elif enabled == 'COUNTRIESS':
            self.cond.add_category(4)
        elif enabled == 'NOT_COUNTRIES':
            self.cond.delete_category(4)
        elif enabled == 'FOOD':
            self.cond.add_category(5)
        elif enabled == 'NOT_FOOD':
            self.cond.delete_category(5)
        elif enabled == 'FRUITS':
            self.cond.add_category(6)
        elif enabled == 'NOT_FRUITS':
            self.cond.delete_category(6)
        print(f'Category set: {self.cond.categories}, {selected}')

    def _create_settings(self, cond):
        item_description_widget: 'pgm.widgets.Label'
        settings = pgm.menu.Menu(
            title="Настройки", height=self._height, width=self._width
        )
        settings.add.selector('',
                              [('Легко', 'EASY'),
                               ('Средне', 'MEDIUM'),
                               ('Сложно', 'HARD')],
                              onchange=self._change_difficulty,
                              selector_id='select_difficulty')
        settings.add.selector('Подсказка',
                              [('Да', True),
                               ('Нет',  False)],
                              onchange=self._change_hint,
                              selector_id='select_hint')
        settings.add.selector('Таймер',
                              [('Да', True),
                               ('Нет', False)],
                              onchange=self._change_timer,
                              selector_id='select_timer')
        settings.add.label('Категории')
        settings.add.selector(
            '',
            items=[('выбрать все', 'ALL'),
                   ('убрать все', 'NONE')],
            onchange=self._change_category,
            selector_id='select_ALL'
        )
        settings.add.selector(
            'Животные',
            items=[('вкл', 'ANIMALS'),
                   ('выкл', 'NOT_ANIMALS')],
            onchange=self._change_category,
            selector_id='select_ANIMALS'
        )
        settings.add.selector(
            'Птицы',
            items=[('вкл', 'BIRDS'),
                   ('выкл', 'NOT_BIRDS')],
            onchange=self._change_category,
            selector_id='select_BIRDS'
        )
        settings.add.selector(
            'Химия',
            items=[('вкл', 'CHEMISTRY'),
                   ('выкл', 'NOT_CHEMISTRY')],
            onchange=self._change_category,
            selector_id='select_CHEMISTRY'
        )
        settings.add.selector(
            'Страны',
            items=[('вкл', 'COUNTRIES'),
                   ('выкл', 'NOT_COUNTRIES')],
            onchange=self._change_category,
            selector_id='select_COUNTRIES'
        )
        settings.add.selector(
            'Еда',
            items=[('вкл', 'FOOD'),
                   ('выкл', 'NOT_FOOD')],
            onchange=self._change_category,
            selector_id='select_FOOD'
        )
        settings.add.selector(
            'Фрукты',
            items=[('вкл', 'FRUITS'),
                   ('выкл', 'NOT_FRUITS')],
            onchange=self._change_category,
            selector_id='select_FRUITS'
        )

        game = self._create_game(self.game_state)

        settings.add.button("Продолжить", post_start_game)
        settings.add.button("Назад", pgm.events.BACK)

        return settings

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
