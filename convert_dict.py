"""
Берёт словарь, состоящий из одного слова на строчку
и преобразует в словарь вида {n: [слова с n уникальными буквами]}
"""

import sys
import json

from collections import defaultdict
from pprint import pprint

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: f{sys.argv[0]} 'dict.txt'")
    
    filename = sys.argv[1]

    content = None
    with open(filename, "r", encoding="utf-8") as fdict:
        content = fdict.read()


    dict = defaultdict(list)
    for word in content.splitlines():
        unique_letters = len(set(word))
        dict[unique_letters].append(word)

    with open(filename, "w", encoding="utf-8") as fdict:
        json.dump(dict, fdict, ensure_ascii=False)