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

# -----------------------------------------------------------------------------
# Part C: Controller Class (replaces ALL globals + free functions)
# -----------------------------------------------------------------------------


class Zoo:

    def __init__(self):
        self._cages = {}
        self._nextAnimalId = 1
        self._speciesRegistry = {
            "lion": Lion,
            "snake": Snake,
            "parrot": Parrot,
        }

    def registerSpecies(self, speciesName, animalCls):
        if not issubclass(animalCls, Animal):
            raise TypeError("animalCls must inherit from Animal.")
        self._speciesRegistry[speciesName.lower()] = animalCls

    def addCage(self, cageId):
        if cageId in self._cages:
            raise ValueError(f"Cage '{cageId}' already exists.")
        self._cages[cageId] = Cage(cageId)

    def addAnimal(self, name, species, cageId):
        if cageId not in self._cages:
            raise ValueError(f"Cage '{cageId}' does not exist.")
        speciesKey = species.lower()
        if speciesKey not in self._speciesRegistry:
            raise ValueError(f"Unknown species '{species}'.")

        animalCls = self._speciesRegistry[speciesKey]
        animal = animalCls(name, self._nextAnimalId)
        self._nextAnimalId += 1
        self._cages[cageId].addAnimal(animal)
        return animal

    def feedAnimal(self, animalId):
        animal = self._find_animal(animalId)
        if animal is None:
            raise ValueError(f"Animal with ID {animalId} not found.")
        return animal.feed()

    def moveAnimal(self, animalId, fromCageId, toCageId):
        if fromCageId not in self._cages:
            raise ValueError(f"Cage '{fromCageId}' does not exist.")
        if toCageId not in self._cages:
            raise ValueError(f"Cage '{toCageId}' does not exist.")

        fromCage = self._cages[fromCageId]
        toCage = self._cages[toCageId]
        animal = next((a for a in fromCage.animals
                       if a.animalId == animalId), None)
        if animal is None:
            raise ValueError(f"""
            Animal {animalId} not found in cage {fromCageId}.""")

        fromCage.removeAnimal(animal)
        toCage.addAnimal(animal)
        return animal

    def rollCall(self, cageId):
        if cageId not in self._cages:
            raise ValueError(f"Cage '{cageId}' does not exist.")
        return [animal.speak() for animal in self._cages[cageId].animals]

    def reportCage(self, cageId):
        if cageId not in self._cages:
            raise ValueError(f"Cage '{cageId}' does not exist.")
        return str(self._cages[cageId])

    def _find_animal(self, animalId):
        for cage in self._cages.values():
            for animal in cage.animals:
                if animal.animalId == animalId:
                    return animal
        return None

