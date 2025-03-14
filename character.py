def create_character():
    print("Welcome to the game! Let's create your character.")
    name = input("What is your name? ")
    name = "Niels"
    print(f"Welcome, {name}!\n")
    
    character = {
        "name": name,
        "race": "Hobbit",
        "class": None
        }

    return character