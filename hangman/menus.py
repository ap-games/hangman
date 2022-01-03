import pygame_menu as pgm
from typing import Tuple
from enum import Enum
import datetime

from hangman.events import *
from hangman.gamestate import GameState, ALPHABET
from hangman.conditions import (
    ALL_CATEGORIES,
    NAME_TO_CAT,
    Conditions,
    Categories,
    Difficulties,
)
from hangman.statistics import Statistics


class Buttons(Enum):
    HINT = "hint_button"
    PAUSE = "pause_button"
    START = "start_button"


class Labels(Enum):
    PLAYED = "label_played"
    WON = "label_won"
    LOST = "label_lost"
    WIN_RATE = "label_win_rate"
    TIMER = "label_timer"


class Menus:
    """
    Создает и хранит в себе игровые меню
    """

    def __init__(
            self,
            width: int,
            height: int,
            conditions: Conditions,
            stats: Statistics,
    ):
        self._height = height
        self._width = width
        self.conditions = conditions
        self.victory = self._create_victory()
        self.defeat = self._create_defeat()
        self.stats = self._create_stats(stats)
        self.pause = self._create_pause()
        self.game = self._create_game()
        self.settings = self._create_settings()
        self.main = self._create_main(self.settings, self.stats)

    def resize(self, width: int, height: int):
        self._width, self._height = width, height
        self.main.resize(width, height)
        self.stats.resize(width, height)
        self.settings.resize(width, height)
        self.victory.resize(width, height)
        self.defeat.resize(width, height)
        self.game.resize(width, height)

    def setup_game(self, conditions: Conditions, game_state: GameState):
        """
        Подготавливает игровое поле к началу новой игры
        """

        timer = self.game.get_widget(Labels.TIMER.value)
        timer.hide()
        if conditions.has_timer:
            timer.show()
        timer.set_title(str(game_state.time_left))

        hint = self.game.get_widget(Buttons.HINT.value)
        hint.hide()
        if conditions.has_hint:
            hint.show()

    def update_timer(self, time_left: datetime.timedelta):
        timer = self.game.get_widget(Labels.TIMER.value)
        timer.set_title(str(time_left.seconds))

    def hide_hint(self):
        self.game.get_widget(Buttons.HINT.value).hide()

    def block_start(self):
        color = pgm.themes.THEME_DEFAULT.readonly_color

        start_button = self.settings.get_widget(Buttons.START.value)
        start_button.set_title("Продолжить (выберите категории)")
        start_button.update_callback(do_nothing)
        start_button.update_font({"color": color, "selected_color": color})

    def allow_start(self):
        color = pgm.themes.THEME_DEFAULT.widget_font_color
        selected_color = pgm.themes.THEME_DEFAULT.selection_color

        start_button = self.settings.get_widget(Buttons.START.value)
        start_button.set_title("Продолжить")
        start_button.update_callback(post_start_game)
        start_button.update_font({"color": color, "selected_color": selected_color})

    def update_stats(self, stats: Statistics):
        played_label = self.stats.get_widget(Labels.PLAYED.value)
        won_label = self.stats.get_widget(Labels.WON.value)
        lost_label = self.stats.get_widget(Labels.LOST.value)
        win_rate_label = self.stats.get_widget(Labels.WIN_RATE.value)

        played_label.set_title(f"Сыграно игр: {stats.played}")
        lost_label.set_title(f"Поражений: {stats.played - stats.won}")
        won_label.set_title(f"Побед: {stats.won}")
        win_rate_label.set_title(f"Винрейт: {stats.win_rate}")

        win_rate_label.show()
        if stats.win_rate is None:
            win_rate_label.hide()

    def _create_stats(self, stats: Statistics):
        stat = pgm.menu.Menu(title="Статистика", height=self._height, width=self._width)

        stat.add.label(f"Сыграно игр: {stats.played}", label_id=Labels.PLAYED.value)
        stat.add.label(f"Побед: {stats.won}", label_id=Labels.WON.value)
        stat.add.label(
            f"Поражений: {stats.played - stats.won}", label_id=Labels.LOST.value
        )
        win_rate_label = stat.add.label(
            f"Винрейт: {stats.win_rate}", label_id=Labels.WIN_RATE.value
        )
        if stats.win_rate is None:
            win_rate_label.hide()

        stat.add.button("Назад", pgm.events.BACK)
        stat.add.button("Сбросить", post_clear_stats)
        return stat

    def _create_settings(self):
        settings = pgm.menu.Menu(
            title="Настройки", height=self._height, width=self._width
        )
        settings.add.selector(
            "",
            [
                (difficulty.translation, name)
                for (name, difficulty) in Difficulties.items()
            ],
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

        for category in Categories:
            settings.add.selector(
                category.value,
                items=[("вкл", category.name), ("выкл", f"NOT_{category.name}")],
                onchange=self._change_category,
                selector_id=f"select_{category.name}",
            )

        settings.add.button("Продолжить", post_start_game, button_id=Buttons.START.value)
        settings.add.button("Назад", pgm.events.BACK)
        return settings

    def _create_main(self, settings, stats):
        main = pgm.menu.Menu(title="Hangman", height=self._height, width=self._width)
        main.add.button("Играть", settings)
        main.add.button("Статистика", stats)
        main.add.button("Выйти", pgm.events.EXIT)
        return main

    def _create_pause(self):
        pause = pgm.menu.Menu(title="Пауза", height=self._height, width=self._width)

        pause.add.button("Продолжить", post_continue)
        pause.add.button("Закончить игру", post_back_to_main)

        return pause

    def _create_game(self):
        game = pgm.menu.Menu(title="Hangman", height=self._height, width=self._width)

        game.add.button("Пауза", post_pause, button_id=Buttons.PAUSE.value)
        game.add.label("", label_id=Labels.TIMER.value)
        game.add.button("Подсказка", post_hint, button_id=Buttons.HINT.value)

        for letter in ALPHABET:
            game.add.button(
                title=letter,
                action=lambda l=letter: post_letter_chosen(l),
                cursor=pgm.locals.CURSOR_HAND
            )

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

    # --- onchange methods ---
    def _change_difficulty(self, _: Tuple[any, int], difficulty: str) -> None:
        self.conditions.difficulty = Difficulties[difficulty]

    def _change_hint(self, _: Tuple, has_hint: bool) -> None:
        self.conditions.has_hint = has_hint

    def _change_timer(self, _: Tuple, has_timer: bool) -> None:
        self.conditions.has_timer = has_timer

    def _change_category(self, _: Tuple, category_name: str) -> None:
        if category_name == "ALL":
            for category in Categories:
                self.settings.get_widget(f"select_{category.name}").set_value("вкл")
                self.conditions.add_category(category)
        elif category_name == "NONE":
            for category in Categories:
                self.settings.get_widget(f"select_{category.name}").set_value("выкл")
                self.conditions.delete_category(category)
        elif NAME_TO_CAT.get(category_name) in ALL_CATEGORIES:
            self.conditions.add_category(NAME_TO_CAT[category_name])
        elif NAME_TO_CAT.get(category_name[4:]) in ALL_CATEGORIES:
            self.conditions.delete_category(NAME_TO_CAT[category_name[4:]])

        if len(self.conditions.categories) == 0:
            self.block_start()
        else:
            self.allow_start()


def do_nothing():
    """
    Функция которая не делает ничего.
    Используется как callback для блокировки кнопок
    """
    pass
