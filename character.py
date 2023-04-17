import random
import math
from location import get_location

class Character:
    def __init__(self, name, level, xp, health, max_health, chakra, max_chakra, element, style, jutsu, hitdie, is_player=True, **attributes):

        self.name = name
        self.level = level
        self.xp = xp
        self.xp_to_next_level = 100
        self.health = health
        self.max_health = max_health
        self.chakra = chakra
        self.max_chakra = max_chakra
        self.element = element
        self.style = style
        self.jutsu = jutsu
        self.strength = attributes.get('strength', 0)
        self.dexterity = attributes.get('dexterity', 0)
        self.constitution = attributes.get('constitution', 0)
        self.intelligence = attributes.get('intelligence', 0)
        self.chakra_control = attributes.get('chakra_control', 0)
        self.charisma = attributes.get('charisma', 0)
        self.attributes = attributes
        self.hitdie = hitdie
        self.is_player = is_player
        self.location = get_location("1")
        self.look()

        if not is_player:
            HPbonus = math.floor((self.attributes['constitution'] - 10) / 2)
            if HPbonus <= 0:
                HPbonus = 0
            lvlhealth = self.hitdie + HPbonus
            self.max_health = self.max_health + (lvlhealth *(self.level - 1))
            lvlchakra = math.floor(self.chakra_control / 2) + (math.floor((self.attributes['intelligence'] - 10 ) / 2))
            self.max_chakra = self.max_chakra + (lvlchakra * (self.level - 1))
            self.health = self.max_health
            self.chakra = self.max_chakra

    def move(self, dir):
        new_location = self.location._neighbors(dir)
        if new_location is None:
            print("You can't go that way!")
        else:
            self.location = get_location(new_location)

    def look(self):
        print(self.location.name)
        print("")
        print(self.location.description)

    def go_n(self, command):
        self.move('n')

    def go_n(self, command):
        self.move('s')

    def go_n(self, command):
        self.move('w')

    def go_n(self, command):
        self.move('e')

    def is_alive(self):

        return self.health > 0

    def take_damage(self, damage):

        self.health -= damage
        self.health = max(self.health, 0)  # Ensure health doesn't go below 0
    
    def gain_xp(self, xp):

        self.xp += xp
        print(f"{self.name} gains {xp} XP.")

        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.xp -= self.xp_to_next_level
        self.level += 1
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        HPbonus = math.floor((self.attributes['constitution'] - 10) / 2)

        if HPbonus <= 0:
            HPbonus = 0

        self.health += self.hitdie + HPbonus
        self.max_health += self.hitdie + HPbonus
        lvlchakra = math.floor(self.chakra_control / 2) + (math.floor((self.attributes['intelligence'] - 10 ) / 2))
        self.chakra += lvlchakra
        self.max_chakra += lvlchakra

        print(f"{self.name} levels up to level {self.level}!")
        print(f"{self.name} gains {self.hitdie} HP and {lvlchakra} Chakra.")
        
        # Let the player choose an attribute to increase
        if self.level  in [4, 8, 12, 16, 19]:

            while True:
                attribute_to_increase = input("Choose an attribute to increase (STR, DEX, CON, INT, CHK, CHA): ").upper()
                if attribute_to_increase in ["STR", "DEX", "CON", "INT", "CHK", "CHA"]:
                    if attribute_to_increase == "STR":
                        self.strength += 1
                    elif attribute_to_increase == "DEX":
                        self.dexterity += 1
                    elif attribute_to_increase == "CON":
                        self.constitution += 1
                    elif attribute_to_increase == "INT":
                        self.intelligence += 1
                    elif attribute_to_increase == "CHK":
                        self.chakra_control += 1
                    elif attribute_to_increase == "CHA":
                        self.charisma += 1
                    print(f"{attribute_to_increase} increased by 1.")
                    break
                else:
                    print("Invalid attribute. Please choose a valid attribute.")

    def roll_1d20(self):
        return random.randint(1, 20)

    def initiative(self):
        return random.randint(1, 20) + math.floor((self.dexterity - 10) / 2)

    def AC(self):
        return 10 + math.floor((self.dexterity - 10) / 2)
        
    def rest(self):
        health_recovered = math.ceil(self.max_health * .3)
        self.health += health_recovered
        if self.health > self.max_health:
            self.health = self.max_health
        return health_recovered

    def meditate(self):
        chakra_recovered = math.ceil(self.max_chakra * .3)
        self.chakra += chakra_recovered
        if self.chakra > self. max_chakra:
            self.chakra = self.max_chakra
        return chakra_recovered
