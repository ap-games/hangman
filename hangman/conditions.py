from enum import Enum


class Difficulty(Enum):
    """
    Сложность игры
    TODO: Обозначить, какие условия на каких сложностях
    """

    EASY = 1
    MEDIUM = 2
    HARD = 3


class Categories(Enum):
    """
    Категории слов для угадывания
    """

    ANIMALS = 1
    BIRDS = 2
    CHEMISTRY = 3
    COUNTRIES = 4
    FOOD = 5
    FRUITS = 6


class Conditions:
    def __init__(
        self, difficulty: Difficulty, categories: set(Categories), cond_timer: bool, cond_hint: bool
    ):
        self._difficulty = difficulty
        self._categories = categories
        self._cond_timer = cond_timer
        self._cond_hint = cond_hint

    def set_cond_timer(self, cond_timer):
        self._cond_timer = cond_timer

    def set_cond_hint(self, cond_hint):
        self._cond_hint = cond_hint

    def set_difficulty(self, value: Difficulty):
        self._difficulty = value

    def add_category(self, value: Categories):
        self.categories.add(value)

    def delete_category(self, value: Categories):
        self.categories.remove(value)

    def set_category(self, value: Categories):
        self.categories.clear()
        self.categories.add(value)

    @property
    def difficulty(self) -> Difficulty:
        return self._difficulty

    @property
    def categories(self) -> set(Categories):
        return self._categories

    @property
    def timer(self) -> bool:
        return self._cond_timer

    @property
    def hint(self) -> bool:
        return self._cond_hint