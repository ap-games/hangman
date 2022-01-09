def do_nothing():
    """
    Функция которая не делает ничего.
    Используется как callback для блокировки кнопок
    """
    pass


DEBUG = True


def dbg_log(msg: str):
    if DEBUG:
        print(f"[dbg] {msg}")
