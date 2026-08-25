# menagerie_legacy.py
# A script to manage a small digital menagerie.

# --- State ---
animals_db = [
    {'id': 1, 'name': 'Leo', 'species': 'lion', 'health': 100, 'cage_id': 'c1'},
    {'id': 2, 'name': 'Kaa', 'species': 'snake', 'health': 80, 'cage_id': 'c2'},
    {'id': 3, 'name': 'Polly', 'species': 'parrot', 'health': 95, 'cage_id': 'c1'},
]
next_animal_id = 4

cages = ['c1', 'c2', 'c3']


# --- Functions ---

def add_animal(name, species, cage_id):
    """Add a new animal to the menagerie and place it in the given cage."""
    global next_animal_id
    global animals_db

    if cage_id not in cages:
        print(f"Error: Cage '{cage_id}' does not exist.")
        return

    new_animal = {
        'id': next_animal_id,
        'name': name,
        'species': species.lower(),
        'health': 100,
        'cage_id': cage_id
    }
    animals_db.append(new_animal)
    print(f"Added {name} the {species} to cage {cage_id}.")
    next_animal_id += 1


def feed_animal(animal_id):
    """Feed the animal with the given ID, increasing its health up to a maximum of 100."""
    animal_found = False
    for animal in animals_db:
        if animal['id'] == animal_id:
            animal['health'] += 10
            if animal['health'] > 100:
                animal['health'] = 100
            print(f"{animal['name']} has been fed. Health is now {animal['health']}.")
            animal_found = True
            break
    if not animal_found:
        print(f"Error: Animal with ID {animal_id} not found.")


def cage_roll_call(cage_id):
    """Print a roll call for the given cage, making each animal in it speak."""
    print(f"\n--- Roll Call for Cage {cage_id} ---")
    animals_in_cage = []
    for animal in animals_db:
        if animal['cage_id'] == cage_id:
            animals_in_cage.append(animal)

    if not animals_in_cage:
        print("The cage is empty.")
        return

    for animal in animals_in_cage:
        sound = ''
        if animal['species'] == 'lion':
            sound = 'roars'
        elif animal['species'] == 'snake':
            sound = 'hisses'
        elif animal['species'] == 'parrot':
            sound = 'squawks'
        else:
            sound = 'makes an unknown sound'

        print(f"{animal['name']} the {animal['species']} {sound}!")


# --- Main Execution ---
if __name__ == "__main__":
    print("Welcome to the Menagerie Management System!")
    print("Initial State:")
    print(animals_db)

    cage_roll_call('c1')
    cage_roll_call('c2')

    print("\nAdding a new animal...")
    add_animal("Scar", "Lion", "c3")

    print("\nFeeding an animal...")
    feed_animal(2)

    print("\nFinal State:")
    cage_roll_call('c1')
    cage_roll_call('c2')
    cage_roll_call('c3')
