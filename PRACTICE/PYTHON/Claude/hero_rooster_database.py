"""
A CLI program storing heroes (name, power, city) in a dictionary. Users can add a hero, search by name, and list all heroes.
Done when: You can add 5 heroes, search for one by name, and display the full roster — all from the terminal.
"""
def add_hero(rooster: dict, name: str, power: str, city: str) -> None:
    rooster[name] = {"power": power, "city": city}

def search_hero(rooster: dict, name: str) -> dict:
    return rooster.get(name, None)

def list_heroes(rooster: dict) -> None:
    for name, details in rooster.items():
        print(f"Name: {name}, Power: {details['power']}, City: {details['city']}")

def main():
    rooster = {}
    add_hero(rooster, "Superman", "Flight, Super Strength", "Metropolis")
    add_hero(rooster, "Batman", "Intellect, Martial Arts", "Gotham")
    add_hero(rooster, "Wonder Woman", "Super Strength, Combat Skills", "Themyscira")
    add_hero(rooster, "Flash", "Super Speed", "Central City")
    add_hero(rooster, "Green Lantern", "Power Ring", "Coast City")
    print("Hero Rooster:")
    list_heroes(rooster)
    search_name = input("Enter hero name to search: ")
    hero = search_hero(rooster, search_name)
    if hero:
        print(f"Found: Name: {search_name}, Power: {hero['power']}, City: {hero['city']}")
    else:
        print(f"Hero '{search_name}' not found.")

if __name__ == "__main__":
    main()