import datetime
import json
import os.path
from itertools import compress
from random import choice

from hangman.conditions import ALL_CATEGORIES, Categories, Conditions, CATEGORY_FILENAME
from hangman.events import *
from hangman.helpers import dbg_log

ALPHABET = list("ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ")


class GameState:
    """
    Хранит текущее состояние игры
    """

    def __init__(self):
        self.time_left: datetime.timedelta = 0
        self.word: str = ""
        self.processed_letters: dict[str, bool] = dict.fromkeys(ALPHABET, False)

        self._lifes: int = 0
        self._left_to_guess: int = 0
        self._hint_used: bool = False
        self._last_measured_time: datetime.datetime = 0

    @property
    def lifes(self) -> int:
        return self._lifes

    def use_hint(self):
        self._hint_used = False

    def new_game(self, conditions: Conditions):
        """
        Приводит GameState к исходному состоянию для начала новой игры.
        """
        self._lifes = conditions.max_lifes
        self._hint_used = not conditions.has_hint
        self.time_left = conditions.difficulty.time_limit

        self.word = self._get_word(
            conditions.categories, conditions.difficulty.letters_to_guess
        )
        self._left_to_guess = len(self.word)

        self._last_measured_time = datetime.datetime.now()
        self.processed_letters = dict.fromkeys(ALPHABET, False)

    def unpause(self):
        """
        Обновляет последнее измеренное время,
        чтобы при снятии игры с паузы таймер не считал паузу за игровое время
        """
        self._last_measured_time = datetime.datetime.now()

    def update_timer(self):
        """
        Обновляет таймер
        Должно вызываться каждый игровой тик
        """
        # не должно вызываться, если condition.has_timer == False
        # if not conditions.has_timer:
        #     return

        now = datetime.datetime.now()
        time_passed = now - self._last_measured_time
        self._last_measured_time = now
        self.time_left -= time_passed
        if self.time_left.total_seconds() <= 0:
            self.time_left = datetime.timedelta(0)  # чтобы не уходило в ноль
            post_lose()

    def _get_word(self, categories: set(Categories), unique_letters: range) -> str:
        """
        Выбирает рандомное слово для угадывания из переданных категорий
        """
        if len(categories) == 0:
            categories = set(ALL_CATEGORIES)

        # выбрать случайную категорию
        random_category = choice(list(categories))

        # открыть словарь этой категории
        category_fname = CATEGORY_FILENAME[random_category]
        path_to_dict = os.path.join("dicts", category_fname)

        # загрузить словарь
        dictionary: dict = None
        with open(path_to_dict, "r", encoding="utf-8") as fdict:
            dictionary = json.load(fdict)

        # выбрать из него слова с подходящим числом уникальных букв
        words_with_matching_ul = []
        for ul in unique_letters:
            dict_ul = dictionary.get(str(ul))
            if dict_ul is not None:
                words_with_matching_ul += dict_ul

        # if len(words_with_matching_ul) == 0:
        #     # этого не должно произойти, если прогнать тесты перед запуском
        #     raise ImportError

        word = choice(words_with_matching_ul)
        dbg_log(f"_get_word(): guessed word: {word}")
        return word

    def process_letter(self, letter: str):
        if self.processed_letters[letter]:
            dbg_log(f"process_letter(): letter {letter} was already chosen!")
            return

        dbg_log(f"process_letter(): chosen letter: {letter}")

        self.processed_letters[letter] = True

        # выводит список букв, которые можно выбрать
        all_letters = list(self.processed_letters.keys())
        chosen = list(self.processed_letters.values())
        not_chosen = [not c for c in chosen]
        left_letters = list(compress(all_letters, not_chosen))
        dbg_log(f"process_letter(): letters left: {''.join(left_letters)}")

        if letter not in self.word:
            self._lifes -= 1
            post_wrong_guess()
        else:
            self._left_to_guess -= self.word.count(letter)

        if self._left_to_guess == 1:
            post_hide_hint()

        if self._left_to_guess > 0 and self._lifes > 0:
            post_continue()
        elif self._lifes == 0:
            post_lose()
        elif self._left_to_guess == 0:  # and self._lifes == 0
            post_win()

        dbg_log(
            "process_letter(): letters left = {}; lifes = {}".format(
                self._left_to_guess, self._lifes
            )
        )
