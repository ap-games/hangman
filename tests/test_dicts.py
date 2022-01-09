import unittest
import os.path
import json
from pathlib import Path

from hangman.conditions import CATEGORY_FILENAME, Difficulties, Difficulty, Categories


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
                    msg=f"Dict {dict_name} doesn't handle difficulty {difficulty.name} \
                    which wants {difficulty.letters_to_guess} unique letters",
                )

    def test_dicts_present(self):
        """
        Проверяет, что файлы словарей существуют
        """
        for category, filename in CATEGORY_FILENAME.items():
            try:
                with open(DICT_DIR / filename, "r") as _:
                    pass
            except FileNotFoundError:
                self.fail(f"Not found dict for category {category.name} (filename '{filename}')")


def dict_handle_difficulty(dict_name: str, difficulty: Difficulty) -> bool:
    dict_path = DICT_DIR / dict_name

    # Открываем словарь
    with open(dict_path, "r", encoding="utf-8") as dict_file:
        dictionary = json.load(dict_file)

    # Проверяем, есть ли в нем слова для заданнго уровня сложности
    words = []
    for uniq_letters in difficulty.letters_to_guess:
        # Загружаем слова с uniq_letters уникальных букв
        dict_ul = dictionary.get(str(uniq_letters))
        if dict_ul is not None:
            words += dict_ul

    if len(words) == 0:
        return False

    return True


if __name__ == "__main__":
    unittest.main()
