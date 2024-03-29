import datetime
from typing import NamedTuple

from hangman.events import *
from hangman.helpers import dbg_log


class Difficulty(NamedTuple):
    """
    Сложность игры
    """

    name: str
    translation: str
    time_limit: datetime.timedelta
    letters_to_guess: range


Difficulties = {
    "EASY": Difficulty(
        name="EASY",
        translation="Легко",
        time_limit=datetime.timedelta(minutes=3),
        letters_to_guess=range(3, 5),
    ),
    "MEDIUM": Difficulty(
        name="MEDIUM",
        translation="Средне",
        time_limit=datetime.timedelta(minutes=2, seconds=30),
        letters_to_guess=range(5, 7),
    ),
    "HARD": Difficulty(
        name="HARD",
        translation="Сложно",
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


CATEGORY_FILENAME = {
    Categories.ANIMALS: "animals.txt",
    Categories.BIRDS: "birds.txt",
    Categories.CHEMISTRY: "chemistry.txt",
    Categories.COUNTRIES: "countries.txt",
    Categories.FOOD: "food.txt",
    Categories.FRUITS: "fruits.txt",
}
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
        self._difficulty = difficulty
        self._categories = categories
        self._has_timer = has_timer
        self._has_hint = has_hint
        self._max_lifes = 8

    def handle_action(self, action: ConditionsChange, value: Any):
        if action == ConditionsChange.DIFFICULTY:
            self.difficulty = value
        elif action == ConditionsChange.HINT:
            self.has_hint = value
        elif action == ConditionsChange.TIMER:
            self.has_timer = value
        elif action == ConditionsChange.ADD_CATEGORY:
            self.add_category(value)
        elif action == ConditionsChange.REMOVE_CATEGORY:
            self.remove_category(value)

    def add_category(self, category: Categories):
        dbg_log(f"add_category(): added category {category}")
        self.categories.add(category)
        if len(self.categories) == 1:
            # если добавили хоть одну категорию, разрешить старт
            post_allow_start()

    def remove_category(self, category: Categories):
        dbg_log(f"remove_category(): removed category {category}")
        self.categories.discard(category)
        if len(self.categories) == 0:
            # если убрали все категории, запретить старт
            post_block_start()

    @property
    def max_lifes(self) -> int:
        return self._max_lifes

    @property
    def categories(self) -> set[Categories]:
        return self._categories

    @property
    def difficulty(self) -> Difficulty:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, difficulty: Difficulty):
        dbg_log(f"difficulty(): difficulty set to {difficulty.name}")
        self._difficulty = difficulty

    @property
    def has_timer(self) -> bool:
        return self._has_timer

    @has_timer.setter
    def has_timer(self, has_timer: bool):
        dbg_log(f"has_timer(): has_timer set to {has_timer}")
        self._has_timer = has_timer

    @property
    def has_hint(self) -> bool:
        return self._has_hint

    @has_hint.setter
    def has_hint(self, has_hint: bool):
        dbg_log(f"has_hint(): has_hint set to {has_hint}")
        self._has_hint = has_hint
