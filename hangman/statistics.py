import json
from json.decoder import JSONDecodeError


class Statistics:
    """
    Обновляет, загружает и выгружает статистику из файла
    """

    def __init__(self, filename: str):
        self._played: int = 0
        self._won: int = 0
        self._filename = filename

        try:
            self._played, self._won = self.read_stats()
        except (FileNotFoundError, JSONDecodeError, KeyError):
            self.write_stats()

    def read_stats(self):
        """
        Считывает статистику из файла
        """

        data = None
        with open(self._filename, "r") as fstat:
            data = fstat.read()
        data = json.loads(data)
        return int(data["played"]), int(data["won"])

    def write_stats(self) -> None:
        """
        Записывает статистику в файл
        """

        stats = {"played": self._played, "won": self._won}

        with open(self._filename, "w") as fstat:
            fstat.write(json.dumps(stats))
            fstat.flush()
        print(f"Written new stats to file: {stats}")

    def clear(self) -> None:
        """
        Обнуляет статистику и записывает в файл
        """

        self._played = 0
        self._won = 0
        self.write_stats()

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
