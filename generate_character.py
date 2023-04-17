import random
import math
import sys
import json
from character import Character
from text_time import text_chunk, text_slow, text_slow_with_delay

# Prints title screen
def title_screen(saved_data):
    game_title()
    if saved_data is not None:
        # Save File Found
        valid_input = menu_existing_game()
    else:
        # No Save File Found
        valid_input = menu_new_game()
    player = option_handler(saved_data, valid_input)
    return player

# Option Handler for new game, load game, or quit
def option_handler(saved_data, valid_input):
    # Player game selection
    while True:
        text_slow("> Enter your command: ", .03)
        option = input("").lower()
        if option in valid_input:
            if option == 'quit':
                            sys.exit()
            elif option in ['load game', 'load']:
                return Character(saved_data.name, saved_data.level, saved_data.xp, saved_data.health, saved_data.max_health, saved_data.chakra, saved_data.max_chakra, 
                        saved_data.element, saved_data.style, saved_data.jutsu, saved_data.hitdie, saved_data.location, saved_data.is_player, **saved_data.attributes) 
            elif option in ['new game', 'new']:
                player = character_creator()
        else:
            print("> Invalid input. Please try again: ")
            continue
        return player

# Player create a character
def character_creator():
    styles = ["taijutsu master", "weapons expert", "ninjutsu specialist", "genjutsu specialist", "senjutsu master", "medical ninja"]
    elements = ["fire", "wind", "lightning", "earth", "water"]
    line1 = "Fire"
    line2 = "Wind"
    line3 = "Lightning"
    line4 = "Earth"
    line5 = "Water"
    text = "[tan]#######################################################################################################################[/tan]\n"\
            "[tan]#[/tan]" + f"[bold bright_red]{line1.center(117)}[/bold bright_red]" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"[bold bright_cyan]{line2.center(117)}[/bold bright_cyan]" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"[bold bright_yellow]{line3.center(117)}[/bold bright_yellow]" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"[bold orange4]{line4.center(117)}[/bold orange4]" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"[bold bright_blue]{line5.center(117)}[/bold bright_blue]" + "[tan]#[/tan]\n"\
            "[tan]#######################################################################################################################[/tan]\n"  
    text_chunk(text, 0.5)
    # Choose Elemental Affinity
    while True:
        text_slow("> What elemental affinity were you born with?: ", .03)
        element = input("").lower()
        print(f"{element}")
        if element in elements:
            break
        else:
            print("Invalid input. Please try again!")
    line1 = "Weapons Expert"
    line2 = "Taijutsu Master"
    line3 = "Ninjutsu Specialist"
    line4 = "Genjutsu Specialist"
    line5 = "Medical Ninja"
    line6 = "Senjutsu Master"
    text ="[tan]#######################################################################################################################[/tan]\n"\
        "[tan]#[/tan]" + f"[bold white]{line1.center(117)}[/bold white]" + "[tan]#[/tan]\n"\
        "[tan]#[/tan]" + f"[bold cyan]{line2.center(117)}[/bold cyan]" + "[tan]#[/tan]\n"\
        "[tan]#[/tan]" + f"[bold yellow]{line6.center(117)}[/bold yellow]" + "[tan]#[/tan]\n"\
        "[tan]#[/tan]" + f"[bold blue]{line3.center(117)}[/bold blue]" + "[tan]#[/tan]\n"\
        "[tan]#[/tan]" + f"[bold magenta]{line4.center(117)}[/bold magenta]" + "[tan]#[/tan]\n"\
        "[tan]#[/tan]" + f"[bold green]{line5.center(117)}[/bold green]" + "[tan]#[/tan]\n"\
        "[tan]#######################################################################################################################[/tan]\n"  
    text_chunk(text, 0.5)
    # Choose a class
    while True:
        text_slow("> What class would you like to start as? ", .03)
        style = input("").lower()
        print(f"{style}")
        if style in styles:
            break
        else:
            print("Invalid input. Please try again!")
    text_slow("> What is your name, shinobi? (You can type 'random' if you'd like the game to choose for you): ", .03)
    # Choose a name
    name = input("")
    if name.lower() == "random":
        name = generate_name()
    attributes, hitdie = select_class(style)
    jutsu = select_jutsu(element)
    player_attributes = attributes
    player_max_health = (hitdie + (player_attributes['constitution'] - 10) // 2)
    player_max_chakra = (math.floor((player_attributes['chakra_control'] - 10) / 2)) + (math.floor((player_attributes['intelligence'] - 10) / 2)) * 5 + 5
    location = "Hidden Leaf Village: Entrance"
    player = Character(name, 1, 0, player_max_health, player_max_health, player_max_chakra, player_max_chakra, element, style, jutsu, hitdie, is_player=True, 
                        **player_attributes)
    return player

# Generate an enemy
def generate_enemy(player_level, player_location):
    styles = ["taijutsu master", "weapons expert", "ninjutsu specialist", "genjutsu specialist", "senjutsu master", "medical ninja"]
    elements = ["fire", "wind", "lightning", "earth", "water"]
    enemy_element, enemy_style = random.choice(elements), random.choice(styles)
    enemy_name = generate_name()
    attributes, hitdie = select_class(enemy_style)
    jutsu = select_jutsu(enemy_element)
    enemy_attributes = attributes
    enemy_max_health = (hitdie + (enemy_attributes['constitution'] - 10) // 2)
    enemy_max_chakra = (math.floor((enemy_attributes['chakra_control'] - 10) / 2)) + math.floor((enemy_attributes['intelligence'] - 10) / 2) * 5 + 5
    enemy = Character(enemy_name, player_level, 0, enemy_max_health, enemy_max_health, enemy_max_chakra, enemy_max_chakra, 
                    enemy_element, enemy_style, jutsu, hitdie, is_player=False, **enemy_attributes)
    return enemy

# Generate a name
def generate_name():
    with open('data/names.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    japanese_names = data['japanese_names']
    naruto_last_names = data['naruto_last_names']
    name = random.choice(japanese_names) + " " + random.choice(naruto_last_names)
    return name

# Class selector
def select_class(style):
    with open('data/starting_classes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    master = data["style"][style]
    attributes = master['attributes']
    hitdie = master['hitdie']
    return attributes, hitdie
def select_jutsu(element):
    with open('data/starting_jutsu.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    justu = data["element"][element]
    return justu

# Game title text
def game_title():
    line1 = "Welcome to 'Naruto: Tales of the Shinobi', a text-based RPG with D&D mechanics"
    line2 = "set in the world of Naruto. In this game, you will create your own ninja"
    line3 = "character and explore the vast and vibrant world of Naruto. You will engage in"
    line4 = "exciting battles against other players and NPCs, using a variety of jutsu and"
    line5 = "techniques inspired by the popular anime and manga series."
    line6 = "[bold gold3]NARUTO: TALES OF THE SHINOBI[/bold gold3]"
    text = "[tan]#######################################################################################################################[/tan]\n"\
    "[tan]#[/tan]" + "============================================ " + f"{line6.center(30)}" + " ===========================================" + "[tan]#[/tan]\n"\
    "[tan]#######################################################################################################################[/tan]\n"\
    "[tan]#[/tan]" + f"{line1.center(117)}" + "[tan]#[/tan]\n"\
    "[tan]#[/tan]" + f"{line2.center(117)}" + "[tan]#[/tan]\n"\
    "[tan]#[/tan]" + f"{line3.center(117)}" + "[tan]#[/tan]\n"\
    "[tan]#[/tan]" + f"{line4.center(117)}" + "[tan]#[/tan]\n"\
    "[tan]#[/tan]" + f"{line5.center(117)}" + "[tan]#[/tan]\n"\
    "[tan]#######################################################################################################################[/tan]"
    text_chunk(text, .3)
# Menu for new game
def menu_new_game():
    print("> SAVE DATA NOT FOUND!")
    line1 = "New Game"
    line2 = "Quit"
    text =  "[tan]#######################################################################################################################[/tan]\n"\
            "[tan]#[/tan]" + f"{line1.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line2.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#######################################################################################################################[/tan]"
    text_chunk(text, 0.1)
    valid_input = ['new game', 'new', 'yes', 'quit']
    return valid_input
# Menu if save file found
def menu_existing_game():
    text_slow_with_delay("> SAVE DATA FOUND!\n", .02, 1)
    line1 = "New Game"
    line2 = "Load Game"
    line3 = "Quit"
    text =  "[tan]#######################################################################################################################[/tan]\n"\
            "[tan]#[/tan]" + f"{line1.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line2.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line3.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#######################################################################################################################[/tan]"
    text_chunk(text, 0.1)
    valid_input = ['new game', 'load game', 'new', 'load', 'quit']
    return valid_input