import pygame as pg

# TODO: разобраться, норм ли это вообще способ создавать свои эвенты

CLEAR_STATS = pg.event.custom_type()


def post_clear_stats():
    pg.event.post(pg.event.Event(CLEAR_STATS))
