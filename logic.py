from json import load, dump
from random import choice
from typing import Any

TOTAL_ATTEMPTS: int = 6

class Country:
    def __init__(self, name: str, info: dict[str, Any]):
        self.Name: str = name
        self.Continent: str = info['ContinentName']
        self.Population: int = info['Population']
        self.Temperature: int = info['Temperature']
        self.Location: tuple = info['CapitalLatitude'], info['CapitalLongitude']

    @property
    def Hemisphere(self) -> str:
        return 'NORTHERN' if self.Location[0] >= 0 else 'SOUTHERN'

class Game:
    def __init__(self):
        self.Attempts: int = 6
        self.GuessedCountries: set[str] = set()
        self.DataGuessedCountries: list[tuple[Any]] = []
        with open('Data/Information.json') as file:
            self._data: dict[str, Any] = load(file)
        self.Target: Country = self._random_country()
        with open('Data/Results.json') as file:
            self.FileLoad: dict[str, Any] = load(file)
        self.FileLoad['NumberOfGames'] += 1

    def _random_country(self) -> Country:
        self.DataNames: list[str] = list(self._data.keys())
        name: str = choice(self.DataNames)
        return Country(name, self._data[name])

    def new_country(self, name) -> Country | None:
        if self.list_checker(name):
            return self.entered_country_data(name)

    def list_checker(self, name) -> bool:
        if self._data.get(name):
            return True
        return False

    def entered_country_data(self, name) -> Country | None:
        if not self.already_guessed(name):
            self.GuessedCountries.add(name)
            return Country(name, self._data[name])

    def already_guessed(self, name: str) -> bool:
        return name in self.GuessedCountries

    def _name(self, country: Country) -> str:
        return f'{TOTAL_ATTEMPTS - self.Attempts}. {country.Name}'

    def _hemisphere_check(self, first: Country, second: Country) -> tuple:
        return first.Hemisphere, first.Hemisphere == second.Hemisphere

    def _continent_check(self, first: Country, second: Country) -> tuple:
        return first.Continent, first.Continent == second.Continent

    def _population_check(self, first: Country, second: Country) -> tuple:
        difference = first.Population - second.Population
        if -500_000 < difference < 500_000:
            return str(first.Population), ('True', difference)
        if -1500_000 < difference < 1500_000:
            return str(first.Population), ('Almost', difference)
        return str(first.Population), ('False', difference)

    def _temperature_check(self, first: Country, second: Country) -> tuple:
        difference = first.Temperature - second.Temperature
        temp = str(first.Temperature) + '°'
        if -1 < difference < 1:
            return temp, ('True', difference)
        if -2 < difference < 2:
            return temp, ('Almost', difference)
        return temp, ('False', difference)

    def _coord_diff(self, first: Country, second: Country) -> tuple:
        return first.Location[0] - second.Location[0], first.Location[1] - second.Location[1]

    def _direction(self, coordinates: tuple) -> str:
        s: str = ''
        s = s + 'S' if 1.5 < coordinates[0] else s if -1.5 <= coordinates[0] <= 1.5 else s + 'N'
        s = s + 'W' if 1.5 < coordinates[1] else s if -1.5 <= coordinates[1] <= 1.5 else s + 'E'
        if len(s) > 0:
            return s, 'Coordinate'
        return 'Target is found', 'True'

    def win_results(self, country: Country):
        self.FileLoad['Wins'] += 1
        if country.Name not in self.FileLoad['Counties']:
            self.FileLoad[country.Continent] += 1
            self.FileLoad['Counties'].append(country.Name)

    def check(self, first: Country, second: Country):
        if first.Name != second.Name:
            self.Attempts -= 1
        data = self._name(first), self._hemisphere_check(first, second), self._continent_check(first, second), \
               self._temperature_check(first, second), self._population_check(first, second), \
               self._direction(self._coord_diff(first, second))
        self.DataGuessedCountries.append(data)

    def end_game(self) -> str:
        with open('Data/Results.json', 'w') as file:
            dump(self.FileLoad, file)
        return self.Target.Name

class ResultsTable:
    def __init__(self):
        with open('Data/Results.json') as file:
            self.FileLoad = load(file)

    def discovered(self) -> str:
        return f'{round(len(self.FileLoad["Counties"]) / 185 * 100, 1):.1f}'

    def continents(self, key: str) -> str:
        TotalNumber = {'Asia': 42, 'Australia': 11, 'Africa': 48, 'Europe': 47, 'America': 37}
        return f'{round(self.FileLoad[key] / TotalNumber[key] * 100, 1):.1f}'
