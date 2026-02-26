import json

# --- all your classes here (Character, Hero, Flash, Villain) ---
class Character:                        # grandparent
    def __init__(self, name):
        self.name = name
    def speak(self):
        print(f"{self.name} says something.")

class Hero(Character):                  # parent
    def __init__(self, name, city):
        super().__init__(name)
        self.city = city
        self.health = 100
    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.name} takes {amount} damage! Health: {self.health}")
    def use_power(self):
        print(f"{self.name} uses a power!")
    def to_dict(self):                  # convert object → dictionary
        return {
            "type": "Hero",
            "name": self.name,
            "city": self.city,
            "health": self.health
        }

class Flash(Hero):                      # child
    def __init__(self, name, city, speed):
        super().__init__(name, city)
        self.speed = speed
    def use_power(self):
        print(f"💨 {self.name} runs at {self.speed:,} m/s!")
    def to_dict(self):                  # Flash adds speed to the dict
        data = super().to_dict()        # get Hero's dict first
        data["type"] = "Flash"
        data["speed"] = self.speed
        return data

class Villain(Hero):
    def __init__(self, name, city, scheme):
        super().__init__(name, city)
        self.scheme = scheme
    def use_power(self):
        print(f"😈 {self.name} uses their power for evil!")
    def reveal_plan(self):
        print(f"🦹 {self.name}'s scheme: {self.scheme}!")
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Villain"
        data["scheme"] = self.scheme
        return data
    
class Superman(Hero):
    def use_power(self):
        print(f"☀️ {self.name} flies over {self.city}!")
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Superman"
        return data

class WonderWoman(Hero):
    def use_power(self):
        print(f"☀️ {self.name} flies over {self.city}!")
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Wonder Woman"
        return data

def save_roster(heroes, filename="roster.json"):
    try:
        data = [h.to_dict() for h in heroes]
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        word = "hero" if len(heroes) == 1 else "heroes"
        print(f"✅ Saved {len(heroes)} {word} to {filename}")
        # ✅ Saved 1 hero to roster.json
        # ✅ Saved 3 heroes to roster.json
    except Exception as e:
        print(f"❌ Failed to save roster: {e}")

def load_roster(filename="roster.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"📂 No roster found at '{filename}' — starting with empty roster.")
        return []
    except json.JSONDecodeError:
        print(f"⚠️ Roster file is corrupted — starting with empty roster.")
        return []

    heroes = []
    for d in data:
        try:
            if d["type"] == "Flash":
                h = Flash(d["name"], d["city"], d["speed"])
            elif d["type"] == "Villain":
                h = Villain(d["name"], d["city"], d["scheme"])
            else:
                h = Hero(d["name"], d["city"])
            h.health = d["health"]
            heroes.append(h)
        except KeyError as e:
            print(f"⚠️ Skipping malformed hero entry — missing field: {e}")

    print(f"📂 Loaded {len(heroes)} heroes from {filename}")
    return heroes

# Build a roster
flash      = Flash("Barry Allen", "Central City", 299792458)
clark      = Hero("Clark Kent", "Metropolis")
eobard     = Villain("Eobard Thawne", "Central City", "destroying the timeline")

roster = [flash, clark, eobard]

# Save it
save_roster(roster)

# Load it back (simulating a fresh program run)
loaded_roster = load_roster()

# Prove it worked
for hero in loaded_roster:
    hero.use_power()

# 💨 Barry Allen runs at 299,792,458 m/s!
# Clark Kent uses a power!
# 😈 Eobard Thawne is destroying the timeline!

# 1. Create 2 heroes and 1 villain
hero1 = Superman("Superman", "Metropolis")
hero2 = WonderWoman("Wonder Woman", "Themyscira")
villain1 = Villain("Lex Luthor", "Metropolis", "taking over the world")

# 2. Save them to roster.json
save_roster([hero1, hero2, villain1])

# 3. Load them back into a new list
loaded_heroes = load_roster()

# 4. Call use_power() on each one
for hero in loaded_heroes:
    hero.use_power()

# 5. Bonus: take_damage() on one hero before saving — does the health restore correctly?
hero1.take_damage(20)
save_roster([hero1, hero2, villain1])
loaded_heroes = load_roster()
for hero in loaded_heroes:
    print(f"{hero.name}: {hero.health} health")

# Test 1 — load when no file exists
import os
if os.path.exists("roster.json"):
    os.remove("roster.json")        # delete it first
loaded = load_roster()              # should handle gracefully

# Test 2 — corrupt the file manually
with open("roster.json", "w") as f:
    f.write("this is not valid json {{{{")
loaded = load_roster()              # should catch JSONDecodeError

# Test 3 — normal flow still works
hero1 = Hero("Superman", "Metropolis")
save_roster([hero1])
loaded = load_roster()