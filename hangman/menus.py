import pygame_menu as pgm
from pygame_menu.locals import ALIGN_RIGHT, ALIGN_LEFT, ALIGN_CENTER, POSITION_CENTER, CURSOR_HAND, POSITION_NORTH
from typing import Tuple
import datetime

from hangman.events import *
from hangman.gamestate import ALPHABET, GameState
from hangman.conditions import (
    ALL_CATEGORIES,
    NAME_TO_CAT,
    Conditions,
    Categories,
    Difficulties,
    Difficulty,
)
from hangman.statistics import Statistics
from pathlib import Path
import os.path

CUR_FILE_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = CUR_FILE_PATH.parent
ASSETS_DIR = ROOT_DIR / "assets"


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


class Images(Enum):
    GALLOWS = "image_gallows"
    TIMER = "image_timer"


class Frames(Enum):
    GUESSED_WORD = "frame_guessed_word"
    CATEGORIES = "frame_categories"


def create_theme() -> pgm.Theme:
    theme = pgm.themes.THEME_DEFAULT.copy()

    # Убрать меню-бар
    theme.title = False

    return theme


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
        self.theme = create_theme()

        self.victory = self._create_victory()
        self.defeat = self._create_defeat()
        self.stats = self._create_stats(stats)
        self.pause = self._create_pause()
        self.game = self._create_game()
        self.settings = self._create_settings(conditions)
        self.main = self._create_main(self.settings, self.stats)

    def resize(self, width: int, height: int):
        self._width, self._height = width, height
        self.main.resize(width, height)
        self.stats.resize(width, height)
        self.settings.resize(width, height)
        self.victory.resize(width, height)
        self.defeat.resize(width, height)
        self.game.resize(width, height)
        self.pause.resize(width, height)

    def setup_game(self, conditions: Conditions, word: str):
        """
        Подготавливает игровое поле к началу новой игры
        """

        # Нарисовать основание виселицы
        self.update_gallows(conditions.max_lifes)

        # Убрать старое угадываемое слово
        guessed_word = self.game.get_widget(Frames.GUESSED_WORD.value)

        old_letters_labels = guessed_word.get_widgets()
        for letter_label in old_letters_labels:
            self.game.remove_widget(letter_label)

        # Подготовить новое угадываемое слово
        for idx, letter in enumerate(word):
            guessed_word.pack(self.game.add.label(title="_", label_id=f"{letter}_{idx}"), align=ALIGN_CENTER)

        # Убрать старые категории
        categories_frame = self.game.get_widget(Frames.CATEGORIES.value)
        old_categories = categories_frame.get_widgets()
        old_categories = old_categories[1:]  # Игнорируем заголовок
        for category_label in old_categories:
            self.game.remove_widget(category_label)

        # Добавить новые категории
        for category in conditions.categories:
            category_label = self.game.add.label(category.value)
            category_label.update_font({"size": 20})
            categories_frame.pack(category_label, align=ALIGN_CENTER, vertical_position=POSITION_NORTH)

        # Подготовить таймер
        timer = self.game.get_widget(Labels.TIMER.value)
        if conditions.has_timer:
            timer.set_title(str(conditions.difficulty.time_limit))
        else:
            timer.set_title("--:--")

        # Подготовить кнопку подсказки
        hint = self.game.get_widget(Buttons.HINT.value)
        hint.hide()
        if conditions.has_hint:
            hint.show()

        # Подготовить клавиатуру (сделать все кнопки рабочими)
        color = pgm.themes.THEME_DEFAULT.widget_font_color
        for letter in ALPHABET:
            letter_button = self.game.get_widget(f"key_{letter}")
            letter_button.update_font({"color": color})
            letter_button.update_callback(lambda l=letter: post_letter_chosen(l))

    def show_hint(self, game_state: GameState):
        game_state.use_hint()
        hint_letter = ""  # буква, которую нужно подсветить
        for letter in game_state.word:
            if not game_state.processed_letters.get(letter):
                hint_letter = letter
                break

        green = (28, 198, 108)
        letter_button = self.game.get_widget(f"key_{hint_letter}")
        letter_button.update_font({"color": green})

    def reveal_letter(self, letter: str):
        guessed_word = self.game.get_widget(Frames.GUESSED_WORD.value)
        letters_labels = guessed_word.get_widgets()

        for letter_label in letters_labels:
            label_id = letter_label.get_id()
            if letter in label_id:
                letter_label.set_title(letter)

    def block_letter(self, letter: str):
        color = pgm.themes.THEME_DEFAULT.readonly_color
        letter_button = self.game.get_widget(f"key_{letter}")
        letter_button.update_callback(do_nothing)
        letter_button.update_font({"color": color})

    def update_gallows(self, lifes: int):
        gallows = self.game.get_widget(Images.GALLOWS.value)
        gallows_image = pgm.BaseImage(ASSETS_DIR / f"gallows_{lifes}.png")
        gallows.set_image(gallows_image)

    def update_timer(self, time_left: datetime.timedelta):
        timer = self.game.get_widget(Labels.TIMER.value)
        timer.set_title(f"{time_left.seconds // 60}:{time_left.seconds % 60:02d}")

    def hide_hint_button(self):
        self.game.get_widget(Buttons.HINT.value).hide()

    def block_start(self):
        color = pgm.themes.THEME_DEFAULT.readonly_color

        start_button = self.settings.get_widget(Buttons.START.value)
        start_button.update_callback(do_nothing)
        start_button.update_font({"color": color, "selected_color": color})

    def allow_start(self):
        color = pgm.themes.THEME_DEFAULT.widget_font_color
        selected_color = pgm.themes.THEME_DEFAULT.selection_color

        start_button = self.settings.get_widget(Buttons.START.value)
        start_button.update_callback(post_start_game)
        start_button.update_font({"color": color, "selected_color": selected_color})

    def update_stats(self, stats: Statistics):
        played_label = self.stats.get_widget(Labels.PLAYED.value)
        won_label = self.stats.get_widget(Labels.WON.value)
        lost_label = self.stats.get_widget(Labels.LOST.value)
        win_rate_label = self.stats.get_widget(Labels.WIN_RATE.value)

        played_label.set_title(f"{stats.played} сыграно игр")
        lost = stats.played - stats.won
        lost_label.set_title(f"{lost} поражений")
        won_label.set_title(f"{stats.won} побед")

        win_rate = int(stats.win_rate * 100) if stats.win_rate is not None else 0
        win_rate_label.set_title(f"{win_rate}% успешных игр")
        win_rate_label.show()
        if stats.win_rate is None:
            win_rate_label.hide()

    def _create_stats(self, stats: Statistics):
        stat = pgm.menu.Menu(title="", height=self._height, width=self._width, theme=self.theme)

        title_label = stat.add.label("Статистика игр")
        delimiter_label = stat.add.label("")

        played_label = stat.add.label(f"{stats.played} сыграно игр", label_id=Labels.PLAYED.value)
        won_label = stat.add.label(f"{stats.won} побед", label_id=Labels.WON.value)
        lost = stats.played - stats.won
        lost_label = stat.add.label(
            f"{lost} поражений", label_id=Labels.LOST.value
        )
        win_rate = int(stats.win_rate * 100) if stats.win_rate is not None else 0
        win_rate_label = stat.add.label(
            f"{win_rate}% успешных игр", label_id=Labels.WIN_RATE.value
        )
        if stats.win_rate is None:
            win_rate_label.hide()

        back_button = stat.add.button("Назад", pgm.events.BACK)
        clear_button = stat.add.button("Сбросить", post_clear_stats)

        frame_max_width = 300

        played_label.set_max_width(frame_max_width)
        lost_label.set_max_width(frame_max_width)
        won_label.set_max_width(frame_max_width)

        stat_frame = stat.add.frame_v(frame_max_width, 350, padding=0)
        stat_frame.pack(title_label, align=ALIGN_CENTER)
        stat_frame.pack(delimiter_label)
        stat_frame.pack(played_label, align=ALIGN_CENTER)
        stat_frame.pack(won_label, align=ALIGN_CENTER)
        stat_frame.pack(lost_label, align=ALIGN_CENTER)
        stat_frame.pack(win_rate_label, align=ALIGN_CENTER)

        buttons_frame = stat.add.frame_h(frame_max_width, 50, padding=0)
        buttons_frame.pack(back_button)
        buttons_frame.pack(clear_button, align=ALIGN_RIGHT)

        return stat

    def _create_settings(self, conditions: Conditions):
        settings = pgm.menu.Menu(
            title="Настройки", height=self._height, width=self._width, theme=self.theme
        )

        difficulty_label = settings.add.label("Сложность")
        difficulty_selector = settings.add.selector(
            "",
            [
                (difficulty.translation, difficulty)
                for difficulty in Difficulties.values()
            ],
            onchange=self._change_difficulty,
            selector_id="select_difficulty",
        )
        delimiter_label = settings.add.label("")
        additional_label = settings.add.label("Доп. условия")
        hint_selector = settings.add.selector(
            "Подсказка: ",
            [("Да", True), ("Нет", False)],
            onchange=self._change_hint,
            selector_id="select_hint",
        )
        timer_selector = settings.add.selector(
            "Таймер: ",
            [("Да", True), ("Нет", False)],
            onchange=self._change_timer,
            selector_id="select_timer",
        )

        additional_frame = settings.add.frame_v(width=400, height=400, padding=0)
        additional_frame.pack(difficulty_label, align=ALIGN_CENTER)
        additional_frame.pack(difficulty_selector, align=ALIGN_CENTER)
        additional_frame.pack(delimiter_label, align=ALIGN_CENTER)
        additional_frame.pack(additional_label, align=ALIGN_CENTER)
        additional_frame.pack(hint_selector, align=ALIGN_CENTER)
        additional_frame.pack(timer_selector, align=ALIGN_CENTER)

        category_label = settings.add.label("Категории")
        multi_category_selector = settings.add.selector(
            "",
            items=[("выбрать все", "ALL"), ("убрать все", "NONE")],
            onchange=self._change_category,
            selector_id="select_ALL",
        )

        category_selectors = []
        for category in Categories:
            category_selector = settings.add.selector(
                category.value + " ",
                items=[("вкл", category.name), ("выкл", f"NOT_{category.name}")],
                onchange=self._change_category,
                selector_id=f"select_{category.name}",
            )
            category_selectors.append(category_selector)

        if len(conditions.categories) == 0:
            post_block_start()

        category_frame = settings.add.frame_v(width=400, height=400, padding=0)
        category_frame.pack(category_label, align=ALIGN_CENTER)
        category_frame.pack(multi_category_selector, align=ALIGN_CENTER)
        for category_selector in category_selectors:
            category_frame.pack(category_selector, align=ALIGN_CENTER)

        conditions_frame = settings.add.frame_h(width=850, height=400, padding=0)
        conditions_frame.pack(category_frame)
        conditions_frame.pack(additional_frame, align=ALIGN_RIGHT)

        start_button = settings.add.button(
            "К игре", post_start_game, button_id=Buttons.START.value
        )
        back_button = settings.add.button("Назад", pgm.events.BACK)

        buttons_frame = settings.add.frame_h(width=400, height=50, padding=0)
        buttons_frame.pack(back_button)
        buttons_frame.pack(start_button, align=ALIGN_RIGHT)

        return settings

    def _create_main(self, settings, stats):
        main = pgm.menu.Menu(title="Hangman", height=self._height, width=self._width, theme=self.theme)
        main.add.button("Играть", settings)
        main.add.button("Статистика", stats)
        main.add.button("Выйти", pgm.events.EXIT)
        return main

    def _create_pause(self):
        pause = pgm.menu.Menu(title="Пауза", height=self._height, width=self._width, theme=self.theme)

        pause.add.button("Продолжить", post_continue)
        pause.add.button("Сдаться", post_back_to_main)

        return pause

    def _create_game(self):
        game = pgm.menu.Menu(title="", height=self._height, width=self._width, theme=self.theme)

        timer_image = game.add.image(ASSETS_DIR / "timer.png", image_id=Images.TIMER.value)
        timer_label = game.add.label("--:-- ", label_id=Labels.TIMER.value)
        pause_button = game.add.button(" II ", post_pause, button_id=Buttons.PAUSE.value)

        timer_label.set_max_width(200)

        header_frame = game.add.frame_h(500, 50, padding=0, align=ALIGN_RIGHT)
        header_frame.pack(pause_button, align=ALIGN_RIGHT)
        header_frame.pack(timer_label, align=ALIGN_RIGHT)
        header_frame.pack(timer_image, vertical_position=POSITION_CENTER, align=ALIGN_RIGHT)

        middle_frame_width = 310

        category_label = game.add.label("Категории")

        category_frame = game.add.frame_v(250, middle_frame_width, padding=0, frame_id=Frames.CATEGORIES.value)
        category_frame.pack(category_label, align=ALIGN_CENTER, vertical_position=POSITION_NORTH)

        gallows_image = game.add.image(ASSETS_DIR / "gallows_8.png", image_id=Images.GALLOWS.value)
        word_frame = game.add.frame_h(40 * 12, 50, padding=0, frame_id=Frames.GUESSED_WORD.value)

        gallows_frame = game.add.frame_v(500, middle_frame_width, padding=0)
        gallows_frame.pack(gallows_image, align=ALIGN_CENTER)
        gallows_frame.pack(word_frame, align=ALIGN_CENTER)

        middle_frame = game.add.frame_h(800, middle_frame_width, padding=0)
        middle_frame.pack(category_frame, align=ALIGN_LEFT)
        middle_frame.pack(gallows_frame, align=ALIGN_CENTER)

        upper_row = game.add.frame_h(40 * 12, 50, padding=0)
        middle_row = game.add.frame_h(40 * 11, 50, padding=0)
        bottom_row = game.add.frame_h(40 * 9, 50, padding=0)

        frames = [upper_row, middle_row, bottom_row]
        qwerty = ["ЙЦУКЕНГШЩЗХЪ", "ФЫВАПРОЛДЖЭ", "ЯЧСМИТЬБЮ"]
        for frame, row in zip(frames, qwerty):
            for letter in row:
                frame.pack(
                    game.add.button(
                        title=letter,
                        action=lambda l=letter: post_letter_chosen(l),
                        cursor=CURSOR_HAND,
                        button_id=f"key_{letter}"
                    )
                )

        hint_button = game.add.button("Подсказка", post_hint, button_id=Buttons.HINT.value)

        keyboard_frame = game.add.frame_v(40 * 12, 200, padding=0, align=ALIGN_CENTER)
        keyboard_frame.pack(upper_row, align=ALIGN_CENTER)
        keyboard_frame.pack(middle_row, align=ALIGN_CENTER)
        keyboard_frame.pack(bottom_row, align=ALIGN_CENTER)
        keyboard_frame.pack(hint_button, align=ALIGN_CENTER)

        return game

    def _create_victory(self):
        victory = pgm.menu.Menu(
            title="Вы выиграли!", height=self._height, width=self._width, theme=self.theme
        )
        victory.add.button("Назад", post_back_to_main)
        return victory

    def _create_defeat(self):
        defeat = pgm.menu.Menu(
            title="Вы проиграли!", height=self._height, width=self._width, theme=self.theme
        )

        defeat.add.image(ASSETS_DIR / "gallows_0.png")

        defeat.add.button("Назад", post_back_to_main)
        return defeat

    # --- onchange methods ---
    @staticmethod
    def _change_difficulty(_: Tuple[any, int], difficulty: Difficulty) -> None:
        post_change_conditions(ConditionsChange.DIFFICULTY, difficulty)

    @staticmethod
    def _change_hint(_: Tuple, has_hint: bool) -> None:
        post_change_conditions(ConditionsChange.HINT, has_hint)

    @staticmethod
    def _change_timer(_: Tuple, has_timer: bool) -> None:
        post_change_conditions(ConditionsChange.TIMER, has_timer)

    def _change_category(self, _: Tuple, category_name: str) -> None:
        if category_name == "ALL":
            for category in Categories:
                self.settings.get_widget(f"select_{category.name}").set_value("вкл")
                post_change_conditions(ConditionsChange.ADD_CATEGORY, category)
        elif category_name == "NONE":
            for category in Categories:
                self.settings.get_widget(f"select_{category.name}").set_value("выкл")
                post_change_conditions(ConditionsChange.REMOVE_CATEGORY, category)
        elif NAME_TO_CAT.get(category_name) in ALL_CATEGORIES:
            category = NAME_TO_CAT[category_name]
            post_change_conditions(ConditionsChange.ADD_CATEGORY, category)
        elif NAME_TO_CAT.get(category_name[4:]) in ALL_CATEGORIES:
            category = NAME_TO_CAT[category_name[4:]]
            post_change_conditions(ConditionsChange.REMOVE_CATEGORY, category)


def do_nothing():
    """
    Функция которая не делает ничего.
    Используется как callback для блокировки кнопок
    """
    pass
