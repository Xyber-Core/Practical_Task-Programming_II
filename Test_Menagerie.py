import unittest
from Menagerie_Refactored import Zoo, Lion, Snake, Parrot, Animal


class TestFeeding(unittest.TestCase):
    def setUp(self):
        self.zoo = Zoo()
        self.zoo.add_cage("c1")
        self.zoo.add_animal("Kaa", "snake", "c1")

    def test_feed_increases_health(self):
        newHealth = self.zoo.feed_animal(1)
        self.assertEqual(newHealth, 100)

    def test_feed_health_cap(self):
        for _ in range(5):
            self.zoo.feed_animal(1)
        animal = self.zoo._find_animal(1)
        self.assertLessEqual(animal.health, 100)

    def test_feed_records(self):
        animal = self.zoo._find_animal(1)
        self.assertEqual(len(animal.feeding_history), 0)
        self.zoo.feed_animal(1)
        self.assertEqual(len(animal.feeding_history), 1)

    def test_feed_unknown_animal_raises(self):
        with self.assertRaises(ValueError):
            self.zoo.feed_animal(999)
