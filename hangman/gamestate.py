from os import path
import pygame as pg
from hangman.conditions import Categories
from hangman.events import *
from random import choice
import os.path

ALPHABET = [
    "А", "Б", "В", "Г", "Д", "Е", "Ж", "И", "Й", "К", "Л", "М", "Н", "О",
    "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь",
    "Э", "Ю", "Я"
]

# dev: возможно, это не лучший способ хранения этой мапы.
# Eсли есть идеи или время на подумать, 
# куда это можно перенести, то вперёд :)
CATEGORY_FILENAME = {
    Categories.ANIMALS: "animals.txt",
    Categories.BIRDS: "birds.txt",
    Categories.CHEMISTRY: "chemistry.txt",
    Categories.COUNTRIES: "countries.txt",
    Categories.FOOD: "food.txt",
    Categories.FRUITS: "fruit.txt",
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
        print("change_word()")

        if len(categories) == 0:
            # TODO: решить, что делать в таком случае 
            # (бросить ошибку? брать слова из всех категорий?)
            print("err: change_word() - no categories specified!")
            categories.append(Categories.ANIMALS)
        
        # выбрать случайную категорию переданного списка
        # тут каст к листу, т.к. нет функций для выбора случайнго элемента из сета
        random_category = choice(list(categories)) 

        # открыть файл, соответствующий этой категории 
        # dev: подумать, стоит ли делать это тут? мб стоит загрузить все слова заранее?
        category_fname = CATEGORY_FILENAME[random_category]
        path_to_dict = os.path.join('dicts', category_fname)

        # выбрать из файла случайное слово
        dict: list = None
        with open(path_to_dict, "r") as fdict:
            dict = fdict.read().splitlines()

        word = choice(dict)
        print(f"dbg: change_word() - new word: {word}")
        word = list(word) # преобразовать слово в лист с буквами
        self.word = word
        self._word_len = len(word)

    def get_hint(self):
        print("get_hint")

        if self._hint == False and self._word_len > 1:
            for letter in self.word:
                print(f"Hint letter: {letter}")

                if self.game_alphabet.get(letter) == False:
                    self.update_state(letter)
                    self._hint = True
                    return self._hint

        return self._hint

    def update_state(self, letter: str):
        self.proc_letter = letter

        print("game_state.update_state()")
        print(f"{self.proc_letter} - LETTER")
        # print(f"CURRENT ALP: \n {self.game_alphabet}")

        if self.game_alphabet.get(self.proc_letter) == False:
            self.game_alphabet.update({self.proc_letter: True})

            print(f"UPD ALP:\n{self.game_alphabet}")

            if self.word.count(letter) == 0: self._lifes -= 1
            else: self._word_len -= self.word.count(letter)

        else:
            print("Letter already proc")
            return self.game_alphabet

        print("word_len = {}, count = {}".format(self._word_len, self._lifes))
        if self._word_len > 0 and self._lifes > 0:
            post_lost(CONTINUE)
            return self.game_alphabet
        elif self._word_len > 0 and self._lifes == 0:
            post_lost(LOSE)
            return self.game_alphabet
        elif self._word_len <= 0 and self._lifes >= 0 and self._lifes != 8:
            post_lost(WIN)
            return self.game_alphabet