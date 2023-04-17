import pickle
from character import Character

# Save System
def load_game():
    try:
        with open("savegame.dat", "rb") as f:
            saved_data = pickle.load(f)
        print("Game loaded.")
        attributes = {
            'strength': saved_data.get('strength', 0),
            'dexterity': saved_data.get('dexterity', 0),
            'constitution': saved_data.get('constitution', 0),
            'intelligence': saved_data.get('intelligence', 0),
            'chakra_control': saved_data.get('chakra_control', 0),
            'charisma': saved_data.get('charisma', 0),
        }
        player = Character(saved_data['name'], saved_data['level'], saved_data['xp'], 
                            saved_data['health'], saved_data['max_health'], saved_data['chakra'], 
                            saved_data['max_chakra'], saved_data['element'], saved_data['style'],
                            saved_data['jutsu'], saved_data['hitdie'], saved_data['is_player'], **attributes)
        if player.is_alive():
            return player
        else:
            print("The loaded player is already dead.")
            reset_choice = input("Do you want to reset the player to their starting state? (y/n)").lower()
            if reset_choice == "y":
                player.reset()
                return player
            else:
                return None
    except FileNotFoundError:
        print("No saved game found.")
        return None

def save_game(player):
    saved_data = {
        'name': player.name,
        'level': player.level,
        'xp': player.xp,
        'health': player.health,
        'max_health': player.max_health,
        'chakra': player.chakra,
        'max_chakra': player.max_chakra,
        'element': player.element,
        'style': player.style,
        'jutsu': player.jutsu,
        'hitdie': player.hitdie,
        'is_player': player.is_player,
        'strength': player.attributes['strength'],
        'dexterity': player.attributes['dexterity'],
        'constitution': player.attributes['constitution'],
        'intelligence': player.attributes['intelligence'],
        'chakra_control': player.attributes['chakra_control'],
        'charisma': player.attributes['charisma'],
}
    with open("savegame.dat", "wb") as f:
        pickle.dump(saved_data, f)
    print("> Game saved.")
