from abc import ABC, abstractmethod
from datetime import datetime

# -----------------------------------------------------------------------------
# Part A: Animal hierarchy (ABC + polymorphic subclasses)
# -----------------------------------------------------------------------------


class Animal(ABC):

    def __init__(self, name, animalId):
        self._name = name
        self._id = animalId
        self._health = 100
        self._feedingHistory = []

    @property
    def name(self):
        return self._name

    @property
    def animalId(self):
        return self._id

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = max(0, min(100, value))

    def feed(self):
        self.health = self.health + 10
        self._feedingHistory.append(datetime.now())
        return self._health

    @property
    def feedingHistory(self):
        return list(self._feedingHistory)

    def lastFed(self):
        return self._feedingHistory[-1] if self._feedingHistory else None

    @abstractmethod
    def speak(self):
        raise NotImplementedError

    def __str__(self):
        return f"""
        {self._name} the {self.__class__.__name__}(Health: {self._health})
        """

    def __repr__(self):
        return (f"""{self.__class__.__name__}(name={self._name!r},
        id={self._id}, health={self._health})""")


class Lion(Animal):
    def speak(self):
        return f"{self._name} Roars!"


class Snake(Animal):
    def speak(self):
        return f"{self._name} Hisses!"


class Parrot(Animal):
    def speak(self):
        return f"{self._name} Squawks!"

# -----------------------------------------------------------------------------
# Part B: Container Class
# -----------------------------------------------------------------------------


class Cage:
    def __init__(self, cageId):
        self._cageId = cageId
        self._animals = []

    @property
    def cageId(self):
        return self._cageId

    def addAnimal(self, animal):
        self._animals.append(animal)

    def removeAnimal(self, animal):
        self._animals.remove(animal)

    @property
    def animals(self):
        return list(self._animals)

    def __str__(self):
        if not self._animals:
            return f"Cage {self._cageId}: (empty)"
        listing = ", ".join(str(a) for a in self._animals)
        return f"Cage {self._cageId}: {listing}"

    def __repr__(self):
        return f"Cage(id={self._cageId!r}, animal_count={len(self._animals)})"

