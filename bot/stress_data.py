from __future__ import annotations
from random import choice

from bot.utils import hide_yo


class StressData:
    stress_table: dict[str, str]
    specifications: dict[str, str]

    def __init__(self, stress_table: dict[str, str], specifications: dict[str, str]):
        self.stress_table = stress_table
        self.specifications = specifications

    def contains(self, word: str) -> bool:
        return word.lower() in self.stress_table

    def generate_task(self) -> str:
        word = choice(tuple(self.stress_table.keys()))
        if word in self.specifications:
            word += " " + self.specifications[word]
        return hide_yo(word)

    def stress(self, word: str) -> str:
        word = word.lower()
        return self.stress_table[word]

    def is_correct(self, stressed_word: str) -> bool:
        word_key = stressed_word.lower()
        check = self.stress_table[word_key] == stressed_word
        yo_check = hide_yo(self.stress_table[word_key]) == stressed_word
        return check or yo_check

    @classmethod
    def from_file(cls, path: str) -> StressData:
        obj = cls({}, {})
        with open(path, mode="r", encoding="utf-8") as file:
            for line in file.readlines():
                word, *other = line.strip().split()
                word_key = word.lower()
                if other:
                    specification = " ".join(other)
                    obj.specifications[word_key] = specification
                obj.stress_table[word_key] = word
                if "ё" in word_key:
                    obj.stress_table[hide_yo(word_key)] = word
        return obj
