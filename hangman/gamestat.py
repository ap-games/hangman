import pygame as pg
from hangman.events import CONTINUE, LOSE, WIN


class GameState:
    """
    Хранит текущее состояние игры
    """

    def __init__(self):
        # Условие игры: 8 попыток
        self._count: int = 8
        # Переприсваивается в функции _create_word() на длину слова
        self._word_len: int = 0
        self.proc_letter: str = "-"
        self.game_alphabet = self._create_alphabet()
        self.proc_alphabet = self.update_state(str)
        self.word = self._create_word()

    def _create_alphabet(self):
        keys = [
            "А", "Б", "В", "Г", "Д", "Е", "Ж", "И", "Й", "К", "Л", "М", "Н", "О",
            "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь",
            "Э", "Ю", "Я"
        ]
        alphabet = dict.fromkeys(keys, False)
        return alphabet

    def _create_word(self):
        # TODO реализовать нормальную работу со словами
        rand_word = "КЛОУН"
        self._word_len = len(rand_word)
        word = list(rand_word)
        print("_create_word(self)")
        return word

    def update_state(self, letter: str):
        self.proc_letter = letter

        print("game_state.update_state()")
        print(f"{self.proc_letter} - LETTER")
        # print(f"CURRENT ALP: \n {self.game_alphabet}")

        if self.game_alphabet.get(self.proc_letter) == False:
            self.game_alphabet.update({self.proc_letter: True})

            print(f"UPD ALP:\n{self.game_alphabet}")

            self._count -= 1
            self._word_len -= self.word.count(letter)
        else:
            print("Letter already proc")
            return self.game_alphabet

        print("word_len = {}, count = {}".format(self._word_len, self._count))
        if self._word_len > 0 and self._count > 0:
            pg.event.post(pg.event.Event(CONTINUE))
            return self.game_alphabet
        elif self._word_len > 0 and self._count == 0:
            pg.event.post(pg.event.Event(LOSE))
            return self.game_alphabet
        elif self._word_len <= 0 and self._count >= 0 and self._count != 8:
            pg.event.post(pg.event.Event(WIN))
            return self.game_alphabet
