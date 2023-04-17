from battle import turn_based_battle
from generate_character import title_screen
from save_system import save_game, load_game
from text_time import text_slow, text_chunk
import json


with open('data/location_map.json', 'r', encoding='utf-8') as f:  
    location_map = json.load(f)

def play_game():
    saved_data = load_game()
    player = title_screen(saved_data)
    # Game Loop
    while player.is_alive():
        get_player_command(player)
        turn_based_battle(player)
        if player.is_alive():
            save_game(player)
            choice = input("> Do you want to continue playing? y/n: ").lower()
            if choice != "y":
                break
    print("> Thanks for playing!")

def get_player_command(player):
    menu_main()
    accecptable_actions = ['move', 'go', 'travel',' walk', 'quit', 'examine', 'interact', 'inspect', 'look']
    while player.is_alive():
        text_slow("> Enter your command: ", .01)
        command = input("").lower()
        if command in accecptable_actions:
            if command == 'move' or 'go' or 'travel' or 'walk':
                move(player)
        else:
            text_slow("> Invalid command. Try again.\n", .01)
            continue

def move(player):
    menu_movement()
    acceptable_actions = ['up', 'down', 'left', 'right']
    while True:
        command = input("").lower()
        if command in acceptable_actions:
            break
        else:
            text_slow("> Invalid command. Try again.\n", .01)
            continue
    while True:
        current_location = player.location
        if command in location_map[current_location][command]:
            current_location = location_map[current_location][command]
            player.location = current_location
            print("You have moved to the " + current_location + ".")
            break
        else:
            print("You cannot move that way.")
            continue

def menu_main():
    line1 = "Move"
    line2 = "Interact"
    line3 = "Examine"
    line4 = "Quit"
    text =  "[tan]#######################################################################################################################[/tan]\n"\
            "[tan]#[/tan]" + f"{line1.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line2.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line3.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line4.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#######################################################################################################################[/tan]"
    text_chunk(text, 0.1)

def menu_movement():
    line1 = "North"
    line2 = "West  +  East"
    line4 = "South"
    text =  "[tan]#######################################################################################################################[/tan]\n"\
            "[tan]#[/tan]" + f"{line1.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line2.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line4.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#######################################################################################################################[/tan]"
    text_chunk(text, 0.1)

# Start the game
play_game()