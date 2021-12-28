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

CATEGORIES_NAMES = ["ANIMALS", "BIRDS", "CHEMISTRY", "COUNTRIES", "FOOD", "FRUITS"]
ALL_CATEGORIES = [
    Categories.ANIMALS,
    Categories.BIRDS,
    Categories.CHEMISTRY,
    Categories.COUNTRIES,
    Categories.FOOD,
    Categories.FRUITS,
]

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

    def add_category(self, category: Categories):
        print("[dbg] added category ", category)
        self.categories.add(category)

    def delete_category(self, category: Categories):
        print("[dbg] removed category ", category)
        self.categories.discard(category)

    def set_category(self, category: Categories):
        print("[dbg] set category ", category)
        self.categories.clear()
        self.categories.add(category)

    @property
    def categories(self) -> set(Categories):
        return self._categories

    @property
    def difficulty(self) -> Difficulty:
        return self._difficulty
    
    @difficulty.setter
    def difficulty(self, difficulty: Difficulty):
        print("[dbg] difficulty set to ", difficulty)
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
