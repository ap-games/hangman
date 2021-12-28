from hangman.conditions import Categories, ALL_CATEGORIES
from hangman.events import *
from random import choice
from itertools import compress
import os.path

ALPHABET = list("ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ")

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
        # Условие игры: 8 попыток
        self._lifes: int = 8
        self._hint = False
        self.proc_letter: str = "-"
        self.game_alphabet = self._create_alphabet()
        self.word: list(str) = ""
        self._word_len: int = 0

    def _create_alphabet(self):
        alphabet = dict.fromkeys(ALPHABET, False)
        return alphabet

    def change_word(self, categories: set(Categories)) -> None:
        """
        Выбирает рандомное слово для угадывания из переданных категорий
        """
        if len(categories) == 0:
            categories = ALL_CATEGORIES

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
        word = list(word)
        self.word = word
        self._word_len = len(word)

    def get_hint(self):
        if self._hint == False and self._word_len > 1:
            for letter in self.word:
                print(f"Hint: {letter}")

                if self.game_alphabet.get(letter) == False:
                    self.update_state(letter)
                    self._hint = True
                    return self._hint

        return self._hint

    def update_state(self, letter: str):
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
