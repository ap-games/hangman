from hangman.conditions import Categories, ALL_CATEGORIES, Conditions
from hangman.events import *
from random import choice
from itertools import compress
import datetime
import os.path

ALPHABET = list("АБВГДЕЖИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")

CATEGORY_FILENAME = {
    Categories.ANIMALS: "animals.txt",
    Categories.BIRDS: "birds.txt",
    Categories.CHEMISTRY: "chemistry.txt",
    Categories.COUNTRIES: "countries.txt",
    Categories.FOOD: "food.txt",
    Categories.FRUITS: "fruits.txt",
}

class GameState:
    """
    Хранит текущее состояние игры
    """

    def __init__(self):
        self.time_left: datetime.timedelta = 0
        self.word: list(str) = ""
        self.proc_letter: str = "-"
        self.game_alphabet = self._create_alphabet()

        self._lifes: int = 0
        self._word_len: int = 0
        self._hint_used: bool = False
        self._last_measured_time: datetime.datetime = 0

    def new_game(self, conditions: Conditions):
        """
        Приводит GameState к исходному состоянию для начала новой игры.
        """
        # dev: в зависимости от condition.difficulty можно давать разное количество жизней
        self._lifes = conditions.max_lifes
        self._hint_used = not conditions.has_hint
        self.word = list(self._get_word(conditions.categories))
        self._word_len = len(self.word)
        self.game_alphabet = self._create_alphabet()

        self._last_measured_time = datetime.datetime.now()
        self.time_left = conditions.time_limit

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
            self.time_left = datetime.timedelta(0) # чтобы не уходило в ноль
            post_lose()

    def _create_alphabet(self):
        alphabet = dict.fromkeys(ALPHABET, False)
        return alphabet

    def _get_word(self, categories: set(Categories)) -> str:
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

        # выбрать из словаря случайное слово
        dict: list = None
        with open(path_to_dict, "r", encoding="utf-8") as fdict:
            dict = fdict.read().splitlines()

        word = choice(dict)
        print(f"[dbg] guessed word: {word}")
        return word

    def get_hint(self):
        if not self._hint_used and self._word_len > 1:
            for letter in self.word:
                print(f"Hint: {letter}")

                if not self.game_alphabet.get(letter):
                    self.process_letter(letter)
                    self._hint_used = True
                    return self._hint_used
        return self._hint_used

    def process_letter(self, letter: str):
        self.proc_letter = letter

        print(f"Chosen letter: {self.proc_letter}")

        if self.game_alphabet.get(self.proc_letter) == False:
            self.game_alphabet.update({self.proc_letter: True})

            all_letters = list(self.game_alphabet.keys())
            chosen = list(self.game_alphabet.values())
            not_chosen = [not c for c in chosen]
            left_letters = list(compress(all_letters, not_chosen))
            print(f"Letters left: {''.join(left_letters)}")

            if self.word.count(letter) == 0:
                self._lifes -= 1
            else:
                self._word_len -= self.word.count(letter)
        else:
            print("Letter {self.proc_letter} was already chosen!")
            return self.game_alphabet

        print("letters left = {}, lifes = {}".format(self._word_len, self._lifes))
        if self._word_len > 0 and self._lifes > 0:
            post_continue()
            return self.game_alphabet
        elif self._word_len > 0 and self._lifes == 0:
            post_lose()
            return self.game_alphabet
        elif self._word_len <= 0 and self._lifes > 0:
            post_win()
            return self.game_alphabet
