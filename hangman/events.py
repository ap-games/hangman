import pygame as pg


CLEAR_STATS = pg.event.custom_type()
CONTINUE = pg.event.custom_type()
LOSE = pg.event.custom_type()
WIN = pg.event.custom_type()


def post_clear_stats():
    pg.event.post(pg.event.Event(CLEAR_STATS))
