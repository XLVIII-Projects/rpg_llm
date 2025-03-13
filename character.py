
def create_character():
    print("Welcome to the game! Let's create your character.")
    name = input("What is your name? ")
    print(f"Welcome, {name}!\n")
    
    character = {
        "name": name,
        "race": "Hobbit",
        "class": None,
        "level": 1,
        "experience": 0,
        "health": 10,
        "max_health": 10,
        "mana": 10,
        "max_mana": 10,
        "location": "The Shire",
    }

    return character