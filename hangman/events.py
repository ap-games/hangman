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
