import math
import random
import sys
from text_time import text_slow, text_slow_with_delay, text_chunk
from rich import print
from rich.console import Console
from rich.table import Table
from generate_character import generate_enemy


console = Console()
# Player Commands
def get_player_command():
    text_slow("> Enter your command: ", .02)
    return input("").lower()

# Battle System
def turn_based_battle(player, enemy):
    enemy = generate_enemy(player_level=player.level, player_location=player.location)
    player_name = get_player_name(player)
    enemy_name = get_enemy_name(enemy)
    text_slow_with_delay(f"> {enemy.name} wants to fight! Roll for initiative!\n", .02, 1)
    player_initiative = player.initiative()
    enemy_initiative = enemy.initiative()
    print(f"> {player_name} ", end=''), text_slow_with_delay(f"rolls a {player_initiative} for initiative!\n", .01, .5)
    print(f"> {enemy_name} ", end=''), text_slow_with_delay(f"rolls a {enemy_initiative} for initiative!\n", .01, .5)
    if player_initiative >= enemy_initiative:
        print(f"> {player_name} ", end=''), text_slow_with_delay(f"goes first.\n", .01, .5)
    else:
        print(f"> {enemy_name} ", end=''), text_slow_with_delay(f"goes first.\n", .01, .5)

    # Battle Loop
    while player.is_alive() and enemy.is_alive():
        if player_initiative >= enemy_initiative:
            print_ui(player, enemy)
            menu_battle()
            run = player_turn(player, enemy, player_name, enemy_name)
            if run == True:
                break
            enemy_turn(enemy, player, enemy_name, player_name)
            if not player.is_alive():
                break
        else:
            print_ui(player, enemy)
            enemy_turn(enemy, player, enemy_name, player_name)
            if not player.is_alive():
                break
            menu_battle()
            run = player_turn(player, enemy, player_name, enemy_name)
            if run == True:
                break
    if not player.is_alive():
        text_slow_with_delay(f"> {enemy.name} defeated {player.name}!\n", .02, .5)
        text_slow_with_delay("> GAME OVER\n", .5, .5)
    elif not enemy.is_alive():
        xp = enemy.level * 50
        player.gain_xp(xp)
        text_slow_with_delay(f"> {player.name} defeated {enemy.name} and gained {xp} XP!\n", .02, .5)

# Attack
def attack(attacker, defender, attacker_name, defender_name):
    attacker_dieroll = attacker.roll_1d20()
    defender_roll = defender.AC()
    attacker_bonus = math.floor((attacker.strength - 10) / 2)
    if attacker_bonus <= 0:
        attacker_bonus = 0
    attacker_roll = attacker_dieroll + attacker_bonus
    print(f"> {attacker_name} ", end=''), text_slow_with_delay(f"attacks up close!\n", .02, .5)
    text_slow_with_delay(f"> They roll a {attacker_dieroll} + {attacker_bonus} ({attacker_roll}) against {defender.name}'s {defender_roll} AC.\n", .02, .5)
    # Successful Attack
    if attacker_roll >= defender_roll:
        damage_roll = random.randint(1, attacker.hitdie)
        damage = damage_roll + attacker_bonus
        if attacker_dieroll >= 20:
            text_slow_with_delay(f"> It's a critical hit! Double damage!\n", .02, .5)
            text_slow_with_delay(f"> They roll a {damage_roll} + {attacker_bonus} ({damage} x 2) for damage.\n", .02, .5)
            damage = damage * 2
        else:
            text_slow_with_delay(f"> They roll a {damage_roll} + {attacker_bonus} ({damage}) for damage.\n", .02, .5)
        defender.take_damage(damage)
        print(f"> {defender_name} ", end=''), text_slow_with_delay(f"takes {damage} damage! Their HP is now {defender.health}/{defender.max_health}.\n", .02, 1.5)
    # Missed Attack
    else:
        print(f"> {attacker_name} ", end=''), text_slow_with_delay(f"missed!.\n", .02, 1.5)

# Cast Jutsu
def cast_jutsu(attacker, defender, jutsu, attacker_name, defender_name):
    attacker_dieroll = attacker.roll_1d20()
    defender_roll = defender.AC()
    attacker_bonus = math.floor((attacker.intelligence - 10) / 2)
    if attacker_bonus <= 0:
        attacker_bonus = 0
    attacker_roll = attacker_dieroll + attacker_bonus
    print(f"> {attacker_name} ", end=''), text_slow_with_delay(f"casts {jutsu['name']}!\n", .02, .5)
    text_slow_with_delay(f"> They roll a {attacker_dieroll} + {attacker_bonus} ({attacker_roll}) against {defender.name}'s {defender_roll} AC.\n", .02, .5)
    if attacker_roll >= defender_roll:
        damage_roll = random.randint(1, jutsu['damage'])
        damage = damage_roll + attacker_bonus
        if attacker_dieroll >= 20:
            text_slow_with_delay(f"> It's a critical hit! Double damage!\n", .02, .5)
            text_slow_with_delay(f"> They deal {damage_roll} + {attacker_bonus} ({damage} x 2) damage.\n", .02, .5)
            damage = damage * 2
        else:
            text_slow_with_delay(f"> They deal {damage_roll} + {attacker_bonus} ({damage}) damage.\n", .02, .5)
        defender.take_damage(damage)
        print(f"> {defender_name} ", end=''),
        text_slow_with_delay(f"takes {damage} damage! Their HP is now {defender.health}/{defender.max_health}.\n", .02, 1)
    # Missed Attack
    else:
        print(f"> {attacker_name} ", end=''), text_slow_with_delay(f"missed!.\n", .02, 1)

# Rest and restore health
def heal(player, enemy, player_name, enemy_name):
    health_recovered = player.rest()
    print(f"> {player_name} ", end='')
    text_slow_with_delay(f"rests and recovers {health_recovered} health\n", .02, .5)
    text_slow_with_delay(f"> Their HP is now {player.health}/{player.max_health}.\n", .02, .5)
    if enemy.is_alive():
        enemy_turn(enemy, player, enemy_name, player_name)

# Meditate and restore Chakra
def meditate(player, enemy, player_name, enemy_name):
    chakra_recovered = player.meditate()
    print(f"> {player_name} ", end='')
    text_slow_with_delay(f"meditates and recovers {chakra_recovered} chakra\n", .02, .5)
    text_slow_with_delay(f"> Their CP is now {player.chakra}/{player.max_chakra}.\n", .02, .5)
    if enemy.is_alive():
        enemy_turn(enemy, player, enemy_name, player_name)

# Player Turn
def player_turn(player, enemy, player_name, enemy_name):
    while player.is_alive() and enemy.is_alive():
        command = get_player_command()
        if command == "heal":
            heal(player, enemy, player_name, enemy_name)
            run = False
            break
        elif command == "meditate":
            meditate(player, enemy, player_name, enemy_name)
            run = False
            break
        elif command == "attack":
            attack(player, enemy, player_name, enemy_name)
            run = False
            break
        elif command == "jutsu":
            jutsu = player.jutsu
            if player.chakra >= jutsu["chakra cost"]:
                player.chakra -= jutsu["chakra cost"]
                cast_jutsu(player, enemy, jutsu, player_name, enemy_name)
                run = False
                break
            else:
                text_slow_with_delay(f"> {player.name} doesn't have enough Chakra to cast {jutsu['name']}!\n", .02, .5)
                continue
        elif command == "run":
            result = random.randint(0, 1)
            if result == 0:
                text_slow_with_delay(f"> {player.name} fails to flee from battle.\n", .02, .5)
                run = False
                break
            else:
                text_slow_with_delay(f"> {player.name} flees from battle!\n", .02, .5)
                run = True
                break
        elif command == "quit":
            sys.exit()
        else:
            text_slow_with_delay("> Invalid command. Try again.\n", .02, 0)
            continue
    return run
# Enemy Turn
def enemy_turn(enemy, player, enemy_name, player_name):
    if enemy.chakra >= enemy.jutsu['chakra cost']:
        attack_type = random.choice(["jutsu", "melee"])
    else:
        attack_type = "melee"
    if attack_type == "jutsu":
        jutsu = enemy.jutsu
        # Enemy Jutsu
        cast_jutsu(enemy, player, jutsu, enemy_name, player_name)
    if attack_type == "melee":
        attack(enemy, player, enemy_name, player_name)

# Get combantant names
def get_player_name(player):
    player_name = player.name
    player_name = f"[bold blue]{player_name}[/bold blue]"
    return player_name
def get_enemy_name(enemy):
    enemy_name = enemy.name
    enemy_name = f"[bold red]{enemy_name}[/bold red]"
    return enemy_name

# Battle menu
def menu_battle():
    line1 = "Attack"
    line2 = "Jutsu" 
    line3 = "Rest"
    line4 = "Meditate"
    line5 = "Run"
    line6 = "Quit"
    text =  "[tan]#######################################################################################################################[/tan]\n"\
            "[tan]#[/tan]" + f"{line1.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line2.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line3.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line4.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line5.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#[/tan]" + f"{line6.center(117)}" + "[tan]#[/tan]\n"\
            "[tan]#######################################################################################################################[/tan]"
    text_chunk(text, .2)

# Enemy UI
def enemy_battle_ui(enemy):
    # Table
    table = Table(show_header=True, header_style="bold red")
    table.add_column("Name", style="dim", width=8)
    table.add_column("Lvl", justify="center", width=3)
    table.add_column("HP", justify="center", width=5)
    table.add_column("CP", justify="center", width=5)
    table.add_column("Element", justify="center", width=10)
    table.add_column("Class", justify="center", width=10)
    table.add_column("Jutsu", justify="center", width=16)
    table.add_column("STR", justify="center", width=4)
    table.add_column("DEX", justify="center", width=4)
    table.add_column("INT", justify="center", width=4)
    table.add_column("CON", justify="center", width=4)
    table.add_column("CHK", justify="center", width=4)
    table.add_column("CHA", justify="center", width=4)
    # Change color of enemy health
    if enemy.health == enemy.max_health:
        health_color = "italic cyan"
    elif enemy.health >= enemy.max_health * 2/3:
        health_color = "italic green"
    elif enemy.health >= enemy.max_health * 1/3:
        health_color = "italic yellow"
    else:
        health_color = "italic red"
    # Change color of enemy chakra
    if enemy.chakra == enemy.max_chakra:
        chakra_color = "italic cyan"
    elif enemy.chakra >= enemy.max_chakra * 2/3:
        chakra_color = "italic green"
    elif enemy.chakra >= enemy.max_chakra * 1/3:
        chakra_color = "italic yellow"
    else:
        chakra_color = "italic red"

    table.add_row(
        f"{enemy.name}",
        f"{enemy.level}",
        f"[{health_color}]{enemy.health}[/{health_color}]/[bold black]{enemy.max_health}[/bold black]",
        f"[{chakra_color}]{enemy.chakra}[/{chakra_color}]/[bold black]{enemy.max_chakra}[/bold black]",
        f"[bold bright_red]Fire[/bold bright_red]" if enemy.element == "fire"
        else f"[bold bright_cyan]Wind[/bold bright_cyan]" if enemy.element == "wind"
        else f"[bold bright_yellow]Lightning[/bold bright_yellow]" if enemy.element == "lightning"
        else f"[bold orange4]Earth[/bold orange4]" if enemy.element == "earth"
        else f"[bold bright_blue]Water[/bold bright_blue]",
        f"[bold cyan]Taijutsu Master[/bold cyan]" if enemy.style == "taijutsu master"
        else f"[bold white]Weapons Expert[/bold white]" if enemy.style == "Weapons Expert"
        else f"[bold blue]Ninjutsu Specialist[/bold blue]" if enemy.style == "Ninjutsu Specialist"
        else f"[bold magenta]Genjutsu Specialist[/bold magenta]" if enemy.style == "Genjutsu Specialist"
        else f"[bold yellow]Senjutsu Master[/bold yellow]" if enemy.style == "Senjutsu Master"
        else f"[bold green]Medical Ninja[/bold green]",
        f"{enemy.jutsu['name']}\nDMG: {enemy.jutsu['damage']} Cost: [italic red]{enemy.jutsu['chakra cost']}[/italic red]",
        f"{enemy.strength}",
        f"{enemy.dexterity}",
        f"{enemy.intelligence}",
        f"{enemy.constitution}",
        f"{enemy.chakra_control}",
        f"{enemy.charisma}",
    )
    console.print(table)

# Player UI
def player_battle_ui(player):
    # Table
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Name", style="dim", width=8)
    table.add_column("Lvl", justify="center", width=3)
    table.add_column("HP", justify="center", width=5)
    table.add_column("CP", justify="center", width=5)
    table.add_column("Element", justify="center", width=10)
    table.add_column("Class", justify="center", width=10)
    table.add_column("Jutsu", justify="center", width=16)
    table.add_column("STR", justify="center", width=4)
    table.add_column("DEX", justify="center", width=4)
    table.add_column("INT", justify="center", width=4)
    table.add_column("CON", justify="center", width=4)
    table.add_column("CHK", justify="center", width=4)
    table.add_column("CHA", justify="center", width=4)
    # Change color of player health
    if player.health == player.max_health:
        health_color = "italic cyan"
    elif player.health >= player.max_health * 2/3:
        health_color = "italic green"
    elif player.health >= player.max_health * 1/3:
        health_color = "italic yellow"
    else:
        health_color = "italic red"
    # Change color of player chakra
    if player.chakra == player.max_chakra:
        chakra_color = "italic cyan"
    elif player.chakra >= player.max_chakra * 2/3:
        chakra_color = "italic green"
    elif player.chakra >= player.max_chakra * 1/3:
        chakra_color = "italic yellow"
    else:
        chakra_color = "italic red"

    table.add_row(
        f"{player.name}",
        f"{player.level}",
        f"[{health_color}]{player.health}[/{health_color}]/[bold black]{player.max_health}[/bold black]",
        f"[{chakra_color}]{player.chakra}[/{chakra_color}]/[bold black]{player.max_chakra}[/bold black]",
        f"[bold bright_red]Fire[/bold bright_red]" if player.element == "fire"
        else f"[bold bright_cyan]Wind[/bold bright_cyan]" if player.element == "wind"
        else f"[bold bright_yellow]Lightning[/bold bright_yellow]" if player.element == "lightning"
        else f"[bold orange4]Earth[/bold orange4]" if player.element == "earth"
        else f"[bold bright_blue]Water[/bold bright_blue]",
        f"[bold cyan]Taijutsu Master[/bold cyan]" if player.style == "taijutsu master"
        else f"[bold white]Weapons Expert[/bold white]" if player.style == "weapons expert"
        else f"[bold blue]Ninjutsu Specialist[/bold blue]" if player.style == "ninjutsu specialist"
        else f"[bold magenta]Genjutsu Specialist[/bold magenta]" if player.style == "genjutsu specialist"
        else f"[bold yellow]Senjutsu Master[/bold yellow]" if player.style == "senjutsu master"
        else f"[bold green]Medical Ninja[/bold green]",
        f"{player.jutsu['name']}\nDMG: {player.jutsu['damage']} Cost: [italic red]{player.jutsu['chakra cost']}[/italic red]",
        f"{player.strength}",
        f"{player.dexterity}",
        f"{player.intelligence}",
        f"{player.constitution}",
        f"{player.chakra_control}",
        f"{player.charisma}",
    )

    console.print(table)

# Print UI
def print_ui(player, enemy):
    player_battle_ui(player)
    enemy_battle_ui(enemy)