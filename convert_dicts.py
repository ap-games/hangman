"""
Берёт словари из папки ./raw_dicts/, состоящий из одного слова на строчку
и преобразует в словари вида {n: [слова с n уникальными буквами]} в папку .dicts/
"""

import json
import os
import os.path

from collections import defaultdict

DICT_DIR = "dicts"
RAW_DICT_DIR = os.path.join(DICT_DIR, "raw_dicts")


def convert_dict(dict_name: str):
    with open(os.path.join(RAW_DICT_DIR, dict_name), "r", encoding="utf-8") as dict_file:
        content = dict_file.read()

    dictionary = defaultdict(list)
    for word in content.splitlines():
        unique_letters = len(set(word))
        dictionary[unique_letters].append(word)

    new_dict_path = os.path.join(DICT_DIR, dict_name)
    with open(new_dict_path, "w", encoding="utf-8") as dict_file:
        json.dump(dictionary, dict_file, ensure_ascii=False, indent=4, sort_keys=True)


if __name__ == "__main__":
    dict_names = [f for f in os.listdir(RAW_DICT_DIR) if os.path.isfile(os.path.join(RAW_DICT_DIR, f))]

    for dict_name in dict_names:
        convert_dict(dict_name)
