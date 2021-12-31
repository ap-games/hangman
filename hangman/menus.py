from os import name, stat
import pygame_menu as pgm
from typing import Tuple
import datetime

from hangman.events import *
from hangman.gamestate import GameState, ALPHABET
from hangman.conditions import Conditions, Categories, Difficulty, ALL_CATEGORIES, CATEGORIES_NAMES
from hangman.statistics import Statistics

class Menus:
    """
    Создает и хранит в себе игровые меню
    """

    def __init__(self,
        width: int,
        height: int,
        conditions: Conditions,
        game_state: GameState,
        stats: Statistics,
    ):
        self._height = height
        self._width = width
        self.conditions = conditions
        self.victory = self._create_victory()
        self.defeat = self._create_defeat()
        self.stats = self._create_stats(stats)
        self.game = self._create_game(game_state)
        self.settings = self._create_settings(game_state)
        self.main = self._create_main(self.settings, self.stats)

    def resize(self, width: int, height: int):
        self._width, self._height = width, height
        self.main.resize(width, height)
        self.stats.resize(width, height)
        self.settings.resize(width, height)
        self.victory.resize(width, height)
        self.defeat.resize(width, height)
        self.game.resize(width, height)

    def _create_stats(self, stats: Statistics):
        stat = pgm.menu.Menu(title="Статистика", height=self._height, width=self._width)

        stat.add.label(f"Сыграно игр: {stats.played}", label_id="played_label")
        stat.add.label(f"Побед: {stats.won}", label_id="won_label")
        stat.add.label(f"Поражений: {stats.played - stats.won}", label_id="lost_label")
        winrate_label = stat.add.label(f"Винрейт: {stats.win_rate}", label_id="winrate_label")
        if stats.win_rate is None:
            winrate_label.hide()

        stat.add.button("Назад", pgm.events.BACK)
        stat.add.button("Сбросить", post_clear_stats)
        return stat

    def setup_game(self, conditions: Conditions, game_state: GameState):
        """
        Подготавливает игровое поле к началу новой игры
        """

        timer = self.game.get_widget("timer_label")
        timer.hide()
        if conditions.has_timer:
            timer.show()
        timer.set_title(str(game_state.time_left))

        hint = self.game.get_widget("hint_button")
        hint.hide()
        if conditions.has_hint:
            hint.show()

    def update_timer(self, time_left: datetime.timedelta):
        timer = self.game.get_widget("timer_label")
        timer.set_title(str(time_left.seconds))

    def hide_hint(self):
        self.game.get_widget("hint_button").hide()

    def update_stats(self, stats: Statistics):
        self.stats.get_widget("played_label").set_title(f"Сыграно игр: {stats.played}")
        self.stats.get_widget("won_label").set_title(f"Побед: {stats.won}")
        self.stats.get_widget("lost_label").set_title(f"Поражений: {stats.played - stats.won}")

        winrate_label = self.stats.get_widget("winrate_label")
        winrate_label.set_title(f"Винрейт: {stats.win_rate}")

        winrate_label.show()
        if stats.win_rate is None:
            winrate_label.hide()

    def _change_difficulty(self, value: Tuple[any, int], difficulty: str) -> None:
        _, index = value
        self.conditions.difficulty = Difficulty(index + 1)

    def _change_hint(self, value: Tuple, enabled: bool) -> None:
        self.conditions.has_hint = enabled

    def _change_timer(self, value: Tuple, enabled: bool) -> None:
        self.conditions.has_timer = enabled

    def _change_category(self, value: Tuple, enabled: str) -> None:
        NOT_CATEGORIES_NAMES = [f"NOT_{category}" for category in CATEGORIES_NAMES]
        name_to_cat = dict(zip(CATEGORIES_NAMES, ALL_CATEGORIES))

        if enabled == "ALL":
            for category_name, category in name_to_cat.items():
                self.settings.get_widget(f"select_{category_name}").set_value("вкл")
                self.conditions.add_category(category)
        elif enabled == "NONE":
            for category_name, category in name_to_cat.items():
                self.settings.get_widget(f"select_{category_name}").set_value("выкл")
                self.conditions.delete_category(category)
        elif enabled in CATEGORIES_NAMES:
            self.conditions.add_category(name_to_cat[enabled])
        elif enabled in NOT_CATEGORIES_NAMES:
            self.conditions.delete_category(name_to_cat[enabled[4:]])

    def _create_settings(self, game_state):
        settings = pgm.menu.Menu(
            title="Настройки", height=self._height, width=self._width
        )
        settings.add.selector(
            "",
            [("Легко", "EASY"), ("Средне", "MEDIUM"), ("Сложно", "HARD")],
            onchange=self._change_difficulty,
            selector_id="select_difficulty",
        )
        settings.add.selector(
            "Подсказка",
            [("Да", True), ("Нет", False)],
            onchange=self._change_hint,
            selector_id="select_hint",
        )
        settings.add.selector(
            "Таймер",
            [("Да", True), ("Нет", False)],
            onchange=self._change_timer,
            selector_id="select_timer",
        )
        settings.add.label("Категории")
        settings.add.selector(
            "",
            items=[("выбрать все", "ALL"), ("убрать все", "NONE")],
            onchange=self._change_category,
            selector_id="select_ALL",
        )

        RUSSIAN_NAMES = ["Животные", "Птицы", "Химия", "Страны", "Еда", "Фрукты"]
        for russian_name, category in zip(RUSSIAN_NAMES, CATEGORIES_NAMES):
            settings.add.selector(
                russian_name,
                items=[("вкл", category), ("выкл", f"NOT_{category}")],
                onchange=self._change_category,
                selector_id=f"select_{category}",
            )

        game = self._create_game(game_state)
        settings.add.button("Продолжить", post_start_game)
        settings.add.button("Назад", pgm.events.BACK)
        return settings

    def _create_main(self, settings, stats):
        main = pgm.menu.Menu(title="Hangman", height=self._height, width=self._width)
        main.add.button("Играть", settings)
        main.add.button("Статистика", stats)
        main.add.button("Выйти", pgm.events.EXIT)
        return main

    def _create_game(self, game_state):
        game = pgm.menu.Menu(title="Hangman", height=self._height, width=self._width)

        game.add.label("", label_id="timer_label")
        game.add.button("Подсказка", post_hint, button_id="hint_button")

        buttons = lambda x: game.add.button(
            x, lambda: game_state.process_letter(x), cursor=pgm.locals.CURSOR_HAND
        )
        for letter in ALPHABET:
            buttons(letter)

        game.add.button("Назад", post_back_to_main)
        return game

    def _create_victory(self):
        victory = pgm.menu.Menu(
            title="Вы выиграли!", height=self._height, width=self._width
        )
        victory.add.button("Назад", post_back_to_main)
        return victory

    def _create_defeat(self):
        defeat = pgm.menu.Menu(
            title="Вы проиграли!", height=self._height, width=self._width
        )
        defeat.add.button("Назад", post_back_to_main)
        return defeat
