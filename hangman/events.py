from pygame import event


CLEAR_STATS = event.custom_type()
HINT = event.custom_type()
CONTINUE = event.custom_type()
LOSE = event.custom_type()
WIN = event.custom_type()
START_GAME = event.custom_type()


def post_clear_stats():
    event.post(event.Event(CLEAR_STATS))


def post_hint():
    event.post(event.Event(HINT))


def post_continue():
    event.post(event.Event(CONTINUE))


def post_win():
    event.post(event.Event(WIN))


def post_lose():
    event.post(event.Event(LOSE))


def post_start_game():
    event.post(event.Event(START_GAME))
