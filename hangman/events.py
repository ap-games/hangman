from enum import Enum
from typing import Any

from pygame import event

CLEAR_STATS = event.custom_type()
HINT = event.custom_type()
PAUSE = event.custom_type()
CONTINUE = event.custom_type()
LOSE = event.custom_type()
WIN = event.custom_type()
START_GAME = event.custom_type()
BACK_TO_MAIN = event.custom_type()
HIDE_HINT = event.custom_type()
LETTER_CHOSEN = event.custom_type()
CHANGE_CONDITIONS = event.custom_type()
BLOCK_START = event.custom_type()
ALLOW_START = event.custom_type()
WRONG_GUESS = event.custom_type()
SURRENDER = event.custom_type()


class ConditionsChange(Enum):
    DIFFICULTY = "CHANGE_DIFFICULTY"
    HINT = "CHANGE_HINT"
    TIMER = "CHANGE_TIMER"
    ADD_CATEGORY = "ADD_CATEGORY"
    REMOVE_CATEGORY = "REMOVE_CATEGORY"


def post_surrender():
    event.post(event.Event(SURRENDER))


def post_wrong_guess():
    event.post(event.Event(WRONG_GUESS))


def post_block_start():
    event.post(event.Event(BLOCK_START))


def post_allow_start():
    event.post(event.Event(ALLOW_START))


def post_change_conditions(change: ConditionsChange, to: Any):
    event.post(event.Event(CHANGE_CONDITIONS, {"action": change, "value": to}))


def post_letter_chosen(letter: str):
    event.post(event.Event(LETTER_CHOSEN, {"letter": letter}))


def post_clear_stats():
    event.post(event.Event(CLEAR_STATS))


def post_hint():
    event.post(event.Event(HINT))


def post_pause():
    event.post(event.Event(PAUSE))


def post_continue():
    event.post(event.Event(CONTINUE))


def post_win():
    event.post(event.Event(WIN))


def post_lose():
    event.post(event.Event(LOSE))


def post_start_game():
    event.post(event.Event(START_GAME))


def post_back_to_main():
    event.post(event.Event(BACK_TO_MAIN))


def post_hide_hint():
    event.post(event.Event(HIDE_HINT))
