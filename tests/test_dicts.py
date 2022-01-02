import unittest
import os.path
import json
from pathlib import Path

from hangman.conditions import Difficulties, Difficulty


CUR_FILE_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = CUR_FILE_PATH.parent
DICT_DIR = ROOT_DIR / "dicts"


class TestDicts(unittest.TestCase):
    """
    Тесты для проверки словарей
    """

    def test_dicts_handle_difficulties(self):
        """
        Проверяет, есть ли подходящие слова в словарях для каждого уровня сложности
        т.к. каждый уровень сложности определяет количество уникальных букв в слове.
        """
        dict_names = [f for f in os.listdir(DICT_DIR) if os.path.isfile(DICT_DIR / f)]

        for dict_name in dict_names:
            for _, difficulty in Difficulties.items():
                self.assertTrue(
                    dict_handle_difficulty(dict_name, difficulty),
                    msg=f"Dict {dict_name} doesn't handle difficulty {difficulty.name} which wants {difficulty.letters_to_guess} unique letters",
                )


def dict_handle_difficulty(dict_name: str, difficulty: Difficulty) -> bool:
    dict_path = DICT_DIR / dict_name

    # Открываем словарь
    dictionary: dict = None
    with open(dict_path, "r", encoding="utf-8") as fdict:
        dictionary = json.load(fdict)

    # Проверяем, есть ли в нем слова для заданнго уровня сложности
    words_with_matching_ul = []
    for ul in difficulty.letters_to_guess:
        dict_ul = dictionary.get(str(ul))
        if dict_ul is not None:
            words_with_matching_ul += dict_ul

    if len(words_with_matching_ul) == 0:
        return False

    return True


if __name__ == "__main__":
    unittest.main()
