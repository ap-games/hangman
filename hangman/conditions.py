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
    TODO: Найти больше категорий и базы слов для них
    """

    ALL = 1
    ANIMALS = 2
    COUNTRIES = 3


class Conditions:
    def __init__(
        self, difficulty: Difficulty, categories: set, timer: bool, hint: bool
    ):
        self._difficulty = difficulty
        self._categories = categories
        self._timer = timer
        self._hint = hint

    @property
    def difficulty(self) -> Difficulty:
        return self._difficulty

    @property
    def categories(self) -> set:
        return self._categories

    @property
    def timer(self) -> bool:
        return self._timer

    @property
    def hint(self) -> bool:
        return self._hint
