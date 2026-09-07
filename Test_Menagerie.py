import unittest
from Menagerie_Refactored import Zoo, Lion, Snake, Parrot, Animal


class TestFeeding(unittest.TestCase):
    def setUp(self):
        self.zoo = Zoo()
        self.zoo.add_cage("c1")
        self.zoo.add_animal("Kaa", "snake", "c1")

    def test_feed_increases_health(self):
        animal = self.zoo._find_animal(1)
        animal.health = 50
        new_health = self.zoo.feed_animal(1)
        self.assertEqual(new_health, 60)

    def test_feed_health_cap(self):
        animal = self.zoo._find_animal(1)
        animal.health = 90

        self.zoo.feed_animal(1)
        self.zoo.feed_animal(1)

        self.assertLessEqual(animal.health, 100)

    def test_feed_records(self):
        animal = self.zoo._find_animal(1)
        self.assertEqual(len(animal.feeding_history), 0)
        self.zoo.feed_animal(1)
        self.assertEqual(len(animal.feeding_history), 1)

    def test_feed_unknown_animal_raises(self):
        with self.assertRaises(ValueError):
            self.zoo.feed_animal(999)


class TestMoveAnimal(unittest.TestCase):
    def setUp(self):
        self.zoo = Zoo()
        self.zoo.add_cage("c1")
        self.zoo.add_cage("c2")
        self.zoo.add_animal("Leo", "lion", "c1")

    def test_move_animal_both_cages_updated(self):
        self.zoo.move_animal(1, "c1", "c2")
        c1_ids = [a.animal_id for a in self.zoo._cages["c1"].animals]
        c2_ids = [a.animal_id for a in self.zoo._cages["c2"].animals]
        self.assertNotIn(1, c1_ids)
        self.assertIn(1, c2_ids)

    def test_move_animal_source_cage_empty(self):
        self.zoo.move_animal(1, "c1", "c2")
        self.assertEqual(self.zoo._cages["c1"].animals, [])
        self.assertEqual(
            str(self.zoo._cages["c1"]),
            "Cage c1: (empty)")

    def test_move_animal_unknown_cage_raises(self):
        with self.assertRaises(ValueError):
            self.zoo.move_animal(1, "c1", "does-not-exist")


class TestSpeciesSpeak(unittest.TestCase):
    def test_lion_roars(self):
        self.assertEqual(Lion("Leo", 1).speak(), "Leo Roars!")

    def test_snake_hisses(self):
        self.assertEqual(Snake("Kaa", 2).speak(), "Kaa Hisses!")

    def test_parrot_squawks(self):
        self.assertEqual(Parrot("Polly", 3).speak(), "Polly Squawks!")

    def test_animal_cannot_be_instantiated_directly(self):
        with self.assertRaises(TypeError):
            Animal("Generic", 4)


class TestSpeciesRegistration(unittest.TestCase):
    def setUp(self):
        self.zoo = Zoo()
        self.zoo.add_cage("c1")

   def test_register_new_species(self):
        class Penguin(Animal):
            def speak(self):
                return f"{self._name} Honks!"

        self.zoo.register_species("penguin", Penguin)
        penguin = self.zoo.add_animal("Rico", "penguin", "c1")

        self.assertIsInstance(penguin, Penguin)
        self.assertEqual(penguin.speak(), "Rico Honks!")

    def test_unknown_species_raises(self):
        with self.assertRaises(ValueError):
            self.zoo.add_animal("Dragon", "dragon", "c1")


if __name__ == "__main__":
    unittest.main()
