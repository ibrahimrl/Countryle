from json import load, dump
from random import choice
from typing import Any

TOTAL_ATTEMPTS: int = 6

class Country:
    def __init__(self, name: str, info: dict[str, Any]):
        self.name: str = name
        self.continent: str = info['ContinentName']
        self.population: int = info['Population']
        self.temperature: int = info['Temperature']
        self.location: tuple[Any, Any] = info['CapitalLatitude'], info['CapitalLongitude']

    @property
    def hemisphere(self) -> str:
        return 'NORTHERN' if self.location[0] >= 0 else 'SOUTHERN'


class Game:
    def __init__(self):
        self.is_finished: bool = False
        self.attempts: int = 6
        self.guessed_countries: set[str] = set()
        self.data_guessed_countries: list[tuple[Any, Any]] = []
        with open('Data/Information.json') as file:
            self._data: dict[str, Any] = load(file)
        self.Target: Country = self._random_country()
        with open('Data/Results.json') as file:
            self.file_load: dict[str, Any] = load(file)
        self.file_load['NumberOfGames'] += 1

    def _random_country(self) -> Country:
        self.data_names: list[str] = list(self._data.keys())
        name: str = choice(self.data_names)
        return Country(name, self._data[name])

    def new_country(self, name: str) -> Country | None:
        if self.list_checker(name):
            return self.entered_country_data(name)
        return None

    def list_checker(self, name: str) -> bool:
        if self._data.get(name):
            return True
        return False

    def entered_country_data(self, name: str) -> Country | None:
        if not self.already_guessed(name):
            self.guessed_countries.add(name)
            return Country(name, self._data[name])
        return None

    def already_guessed(self, name: str) -> bool:
        return name in self.guessed_countries

    def _name(self, country: Country) -> tuple[str, str]:
        return str(TOTAL_ATTEMPTS - self.attempts), country.name

    def _hemisphere_check(self, first: Country, second: Country) -> tuple[str, bool]:
        return first.hemisphere, first.hemisphere == second.hemisphere

    def _continent_check(self, first: Country, second: Country) -> tuple[str, bool]:
        return first.continent.upper(), first.continent == second.continent

    def _population_check(self, first: Country, second: Country) -> tuple[str, tuple[str, int]]:
        return formatting_population(first.population), self._check_difference(first.population, second.population,
                                                                               500_000, 1_500_000)

    def _temperature_check(self, first: Country, second: Country) -> tuple[str, tuple[str, int]]:
        return str(first.temperature) + '°', self._check_difference(first.temperature, second.temperature, 1, 2)

    def _check_difference(self, first, second, close, almost) -> tuple[str, int]:
        difference = abs(first - second)
        status = 'False'

        if difference < close:
            status = 'True'
        elif difference < almost:
            status = 'Almost'
        return status, difference

    def _coord_diff(self, first: Country, second: Country) -> tuple[int, int]:
        return first.location[0] - second.location[0], first.location[1] - second.location[1]

    def _direction(self, coordinates: tuple[int, int]) -> tuple[str, str]:
        s: str = ''
        s = s + 'S' if 1.5 < coordinates[0] else s if -1.5 <= coordinates[0] <= 1.5 else s + 'N'
        s = s + 'W' if 1.5 < coordinates[1] else s if -1.5 <= coordinates[1] <= 1.5 else s + 'E'
        if len(s) > 0:
            return s, 'Coordinate'
        return 'Target is found', 'True'

    def win_results(self, country: Country):
        self.file_load['Wins'] += 1
        if country.name not in self.file_load['Counties']:
            self.file_load[country.continent] += 1
            self.file_load['Counties'].append(country.name)

    def check(self, first: Country, second: Country):
        if first.name != second.name:
            self.attempts -= 1
        data = self._name(first), self._hemisphere_check(first, second), self._continent_check(first, second), \
               self._temperature_check(first, second), self._population_check(first, second), \
               self._direction(self._coord_diff(first, second))
        self.data_guessed_countries.append(data)

    def end_game(self) -> str | None:
        if not self.is_finished:
            self.is_finished = True
            with open('Data/Results.json', 'w') as file:
                dump(self.file_load, file)
            return self.Target.name
        return None

def formatting_population(name: int) -> str:
    num_str: str = str(name)
    n: int = len(num_str)
    match n:
        case 4 | 5 | 6:
            return f'{num_str[:n-3]}.{num_str[n-3]}K'
        case 7 | 8 | 9:
            return f'{num_str[:n - 6]}.{num_str[n - 6]}M'
        case 10 | 11 | 12:
            return f'{num_str[:n - 9]}.{num_str[n - 9]}B'
        case _:
            return num_str


class ResultsTable:
    def __init__(self):
        with open('Data/Results.json') as file:
            self.file_load = load(file)

    def game_number(self) -> int:
        return self.file_load["NumberOfGames"]

    def win_number(self) -> int:
        return self.file_load["Wins"]

    def discovered(self) -> str:
        return f'{round(len(self.file_load["Counties"]) / 185 * 100, 1):.1f}%'

    def continents(self) -> dict[str, str]:
        results: dict[str, str] = {}
        total_number: dict[str, int] = {'Asia': 42, 'Australia': 11, 'Africa': 48, 'Europe': 47, 'America': 37}
        for c in total_number.keys():
            results[c] = f'{round(self.file_load[c] / total_number[c] * 100, 1):.1f}%'
        return results
