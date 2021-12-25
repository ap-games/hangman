import pygame as pg
from hangman.events import *

ALPHABET = [
    "А", "Б", "В", "Г", "Д", "Е", "Ж", "И", "Й", "К", "Л", "М", "Н", "О",
    "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь",
    "Э", "Ю", "Я"
]

class GameState:
    """
    Хранит текущее состояние игры
    """

    def __init__(self):
        # Условие игры: 8 попыток
        self._lifes: int = 8
        # Переприсваивается в функции _create_word() на длину слова
        self._word_len: int = 0
        self._hint = False
        self.proc_letter: str = "-"
        self.game_alphabet = self._create_alphabet()
        self.word = self._create_word()

    def _create_alphabet(self):
        alphabet = dict.fromkeys(ALPHABET, False)
        return alphabet

    def _create_word(self):
        # TODO реализовать нормальную работу со словами
        rand_word = "КЛОУН"
        self._word_len = len(rand_word)
        word = list(rand_word)
        print("_create_word(self)")
        return word

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