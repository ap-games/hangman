class Statistics:
    """
    Обновляет, загружает и выгружает статистику из файла
    """

    def __init__(self, filename: str):
        self._played: int = 0
        self._won: int = 0
        self._filename = filename  # TODO: Подумать над куда положить файл
        # TODO: Открыть файл и считать статистику, или создать файл статистики, если его нет

    def flush(self) -> None:
        """
        Записывает статистику в файл
        # TODO: Реализовать
        """
        pass

    def clear(self) -> None:
        """
        Обнуляет статистику и записывает в файл
        """
        self._played = 0
        self._won = 0
        self.flush()

    @property
    def played(self) -> int:
        return self._played

    @played.setter
    def played(self, value: int):
        self._played = value

    @property
    def won(self) -> int:
        return self._won

    @won.setter
    def won(self, value: int):
        self._won = value

    @property
    def lost(self) -> int:
        return self._played - self._won

    @property
    def win_rate(self) -> float:
        return round(self._won / self._played, 2)
