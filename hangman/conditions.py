from enum import Enum
from typing import TypedDict
import datetime


class Difficulty(TypedDict):
    """
    Сложность игры
    """

    name: str
    translation: str
    max_lifes: int
    time_limit: datetime.timedelta
    letters_to_guess: range


Difficulties = {
    "EASY": Difficulty(
        name="EASY",
        translation="Легко",
        max_lifes=8,
        time_limit=datetime.timedelta(minutes=3),
        letters_to_guess=range(3, 5),
    ),
    "MEDIUM": Difficulty(
        name="MEDIUM",
        translation="Средне",
        max_lifes=6,
        time_limit=datetime.timedelta(minutes=2, seconds=30),
        letters_to_guess=range(5, 7),
    ),
    "HARD": Difficulty(
        name="HARD",
        translation="Сложно",
        max_lifes=4,
        time_limit=datetime.timedelta(minutes=2),
        letters_to_guess=range(7, 10),
    ),
}


class Categories(Enum):
    """
    Категории слов для угадывания
    """

    ANIMALS = "Животные"
    BIRDS = "Птицы"
    CHEMISTRY = "Химия"
    COUNTRIES = "Страны"
    FOOD = "Еда"
    FRUITS = "Фрукты"


ALL_CATEGORIES = [category for category in Categories]
NAME_TO_CAT = {category.name: category for category in Categories}


class Conditions:
    def __init__(
        self,
        difficulty: Difficulty,
        categories: set[Categories],
        has_timer: bool,
        has_hint: bool,
    ):
        self.max_lifes = 8
        self.time_limit = datetime.timedelta(seconds=60)
        self._difficulty = difficulty
        self._categories = categories
        self._has_timer = has_timer
        self._has_hint = has_hint

    def add_category(self, category: Categories):
        print("[dbg] added category ", category)
        self.categories.add(category)

    def delete_category(self, category: Categories):
        print("[dbg] removed category ", category)
        self.categories.discard(category)

    @property
    def categories(self) -> set[Categories]:
        return self._categories

    @property
    def difficulty(self) -> Difficulty:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, difficulty: Difficulty):
        print("[dbg] difficulty set to ", difficulty["name"])
        self._difficulty = difficulty

    @property
    def has_timer(self) -> bool:
        return self._has_timer

    @has_timer.setter
    def has_timer(self, has_timer: bool):
        print("[dbg] has_timer set to ", has_timer)
        self._has_timer = has_timer

    @property
    def has_hint(self) -> bool:
        return self._has_hint

    @has_hint.setter
    def has_hint(self, has_hint: bool):
        print("[dbg] has_hint set to ", has_hint)
        self._has_hint = has_hint
